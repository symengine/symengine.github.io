require "rake"
require "mkmf" # for find_executable
require "fileutils" # Cross Platform

#############
# Variables #
#############
# Common
CWD = File.expand_path(__dir__)
OUTPUB = File.join(CWD, "public")
# Site
BASESITE = File.join(CWD, "docs")
# Files
docFiles = FileList['docs/**/*.myst.md'] do |fl|
    fl.exclude do |f| 
      `git ls-files #{f}`.empty?
    end
end

# Exception
class RunnerException < StandardError
  def initialize(msg = "Undefined runner, currently supports only conda", exception_type = "custom")
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
task :default => :writeDocs

desc "Clean the generated content"
task :clean do
  rm_rf "public"
end

desc "Serve and write docs with sphinx-autobuild"
task :writeDocs, [:port, :runner] do |task, args|
  args.with_defaults(:port => "1337", :runner => "conda")
  if args.runner == "conda"
    sh "conda run sphinx-autobuild #{BASESITE} #{OUTPUB} --port #{args.port}"
  else
    raise RunnerException.new
  end
end

desc "Generate all the notebooks from markdown"
task :genJup => docFiles.ext(".ipynb")

rule ".ipynb" => ".md" do |t|
  sh "jupytext --from myst --to ipynb #{File.join(CWD,t.source)}"
end

desc "Generate content for the notebooks branch"
task :genNotebooks => ["genJup"] do |t|
  FileUtils.mkdir_p("#{NBSITE}")
  cp_r(Dir["#{BASESITE}/."], "#{NBSITE}")
end

# Generate notebooks <-> markdown
# https://github.com/executablebooks/sphinx-autobuild
# https://github.com/executablebooks/MyST-Parser/issues/263

# Site 
namespace "site" do
  desc "Build full site"
  task :mkDocs, [:builder, :runner] do |taks, args|
    args.with_defaults(:builder => "html", :runner => "conda")
    Rake::Task["site:mkSphinx"].invoke(args.builder, args.runner)
  end
  desc "Build site with sphinx"
  task :mkSphinx, [:builder, :runner] do |task, args|
    args.with_defaults(:builder => "html", :runner => "conda")
    if args.runner == "conda"
      sh "conda run sphinx-build #{BASESITE} #{OUTPUB} -b #{args.builder}"
    else
      raise RunnerException.new
    end
  end
end
