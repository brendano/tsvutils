# go through tsv as universal intermediary

mode = ARGV[0]
(mode=="clean" || mode=="make") or raise "Must give argument 'clean' or 'make'"

$sources = %w(csv eq json ssv uniq xlsx yaml fmt)
$dests =   %w(csv fmt html my tex ssv)

# do the options go to the right-side command, or left-side command?
$opts_right = /.*2fmt/

system "mkdir -p bridges"

def make_bridge_list()
  bridges = []
  for s in $sources
    for d in $dests
      # next if s==d
      left = "#{s}2tsv"
      right = "tsv2#{d}"
      if File.exists?(left) && File.exists?(right)
        if "#{s}2#{d}" =~ $opts_right
          right = %|#{right} "$@"|
        else
          left  = %|#{left} "$@"|
        end
        bridges << "#{s}2#{d}"
      end
    end
  end
  bridges
end

bridges = make_bridge_list()

for bridge in bridges do
  s,d = bridge.split("2")
  left = "#{s}2tsv"
  right = "tsv2#{d}"

  if mode=="make"
    open("bridges/#{s}2#{d}","w") do |f|
      f.puts %[
      #!/bin/sh
      #{left} | #{right}
      ].gsub(/^ */,"").strip
    end
    system "chmod +x bridges/#{s}2#{d}"
    system "ln -s bridges/#{s}2#{d} ." if !File.exists?("#{s}2#{d}")
  elsif mode=="clean"
    system "rm -f #{s}2#{d}"
    system "rm -f bridges/#{s}2#{d}"
  end
end

if mode=="make"
  gitignore = open(".gitignore").read
  gitignore.sub!(/BRIDGES_BELOW.*/, (["BRIDGES_BELOW"] + bridges).join("\n"))
  open(".gitignore",'w'){|f| f.puts gitignore }
end
