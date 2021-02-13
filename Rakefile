require "rake"
require "mkmf" # for find_executable
require "fileutils" # Cross Platform

#############
# Variables #
#############
# Common
CWD = File.expand_path(__dir__)
DOXYFILE = "Doxyfile-syme.cfg"
NIXSHELL = File.join(CWD, "shell.nix")
SYMESRC = File.join(CWD, "projects/symengine/symengine")
OUTPUB = File.join(CWD, "public")
# Site
BASESITE = File.join(CWD, "docs")
GENSITE = File.join(BASESITE, "_build")
# Files
docFiles = FileList['docs/**/*.md'] do |fl| 
    fl.exclude do |f| 
      `git ls-files #{f}`.empty?
    end
end
 

# Exception
class RunnerException < StandardError
  def initialize(msg = "Undefined runner, supports nix and system (with conda)", exception_type = "custom")
    @exception_type = exception_type
    super(msg)
  end
end

class ExecException < StandardError
  def initialize(msg = "Missing an application, typically doxyrest", exception_type = "custom")
    @exception_type = exception_type
    super(msg)
  end
end

#########
# Tasks #
#########

# Genric
task :default => :darkServe

desc "Clean the generated content"
task :clean do
  rm_rf "public"
  rm_rf "docs/_build"
end

desc "Serve site with darkhttpd"
task :darkServe, [:port, :runner] do |task, args|
  args.with_defaults(:port => "1337", :runner => "system")
  if args.runner == "system"
    sh "darkhttpd #{CWD} --port #{args.port}"
  elsif args.runner == "nix"
    sh "nix-shell #{NIXSHELL} --run 'darkhttpd #{CWD} --port #{args.port}'"
  else
    raise RunnerException.new
  end
end

desc "Generate all the notebooks from markdown"
task :genJup => docFiles.ext(".ipynb")

rule ".ipynb" => ".md" do |t|
  sh "jupytext --to ipynb #{File.join(CWD,t.source)}"
end

# Maybe a better browsersync setup
# Generate notebooks <-> markdown
# https://github.com/executablebooks/sphinx-autobuild
# https://github.com/executablebooks/MyST-Parser/issues/263

# Site 

namespace "site" do
  desc "Build full site"
  task :mkDocs, [:builder, :runner] do |taks, args|
    args.with_defaults(:builder => "html", :runner => "system")
    Rake::Task["site:mkSphinx"].invoke(args.builder, args.runner)
  end
  desc "Build site with jupyter-book"
  task :mkSphinx, [:builder, :runner] do |task, args|
    args.with_defaults(:builder => "html", :runner => "system")
    if args.runner == "system"
      sh "conda run jupyter-book build #{BASESITE} --builder #{args.builder}"
    elsif args.runner == "nix"
      begin
        sh "nix-shell #{NIXSHELL} --run 'jupyter-book build #{BASESITE} -b #{args.builder}'"
      rescue
        puts "Handling the case where nix errors out by rescuing with conda"
        sh "conda run jupyter-book build #{BASESITE} --builder #{args.builder}"
      end
    else
      raise RunnerException.new
    end
    puts "Moving files to the right location..."
    FileUtils.mkdir_p OUTPUB
    puts "... Also preventing trigger happy gh-pages rubbish"
    sh "touch #{OUTPUB}/.nojekyll"
    sh "echo symengine.org > #{OUTPUB}/CNAME"
    Dir.glob(File.join(GENSITE,"html","*")).each do|file|
      FileUtils.move file, File.join(OUTPUB, File.basename(file))
    end
  end
end
