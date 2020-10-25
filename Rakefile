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
# Wiki
BASEWIKI = File.join(CWD, "docs/wiki")
GENWIKI = File.join(BASEWIKI, "_build")
OUTWIKI = File.join(CWD, "public", "wiki")

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
  rm_rf "docs/wiki/_build"
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

# Maybe a better browsersync setup
# Generate notebooks <-> markdown
# https://github.com/executablebooks/sphinx-autobuild
# https://github.com/executablebooks/MyST-Parser/issues/263

# Wiki 

namespace "wiki" do
  desc "Build full wiki"
  task :mkDocs, [:builder, :runner] do |taks, args|
    args.with_defaults(:builder => "html", :runner => "system")
    Rake::Task["wiki:mkSphinx"].invoke(args.builder, args.runner)
  end
  desc "Build wiki with jupyter-book"
  task :mkSphinx, [:builder, :runner] do |task, args|
    args.with_defaults(:builder => "html", :runner => "system")
    if args.runner == "system"
      sh "conda run jupyter-book build #{BASEWIKI} --builder #{args.builder}"
    elsif args.runner == "nix"
      begin
        sh "nix-shell #{NIXSHELL} --run 'jupyter-book build #{BASEWIKI} -b #{args.builder}'"
      rescue
        puts "Handling the case where nix errors out by rescuing with conda"
        sh "conda run jupyter-book build #{BASEWIKI} --builder #{args.builder}"
      end
    else
      raise RunnerException.new
    end
    puts "Moving files to the right location"
    FileUtils.mkdir_p OUTWIKI
    # sh "cp -rf #{File.join(GENWIKI,"html")}/* #{OUTWIKI}"
    Dir.glob(File.join(GENWIKI,"html","*")).each do|file|
      FileUtils.move file, File.join(OUTWIKI, File.basename(file))
    end
  end
end
