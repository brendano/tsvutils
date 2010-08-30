# go through tsv as universal intermediary

sources = %w(csv eq json ssv uniq xlsx yaml)
dests =   %w(csv fmt html my tex)

bridges = []

for s in sources
  for d in dests
    # next if s==d
    left = "#{s}2tsv"
    right = "tsv2#{d}"
    if File.exists?(left) && File.exists?(right)
      puts "making #{s}2#{d}"
      open("bridges/#{s}2#{d}","w") do |f|
        f.puts %[
        #!/bin/sh
        #{left} "$@" | #{right}
        ].gsub(/^ */,"").strip
      end
      bridges << "#{s}2#{d}"
      system "chmod +x bridges/#{s}2#{d}"
      system "ln -s bridges/#{s}2#{d} ." if !File.exists?("#{s}2#{d}")
    end
  end
end

gitignore = open(".gitignore").read
gitignore.sub!(/BRIDGES_BELOW.*/, (["BRIDGES_BELOW"] + bridges).join("\n"))
open(".gitignore",'w'){|f| f.puts gitignore }
