require 'rake'
require 'mkmf' # for find_executable

# Variables
CWD = File.expand_path(__dir__)
DOXYFILE = "Doxyfile-syme.cfg"
NIXSHELL = File.join(CWD, "shell.nix")
OUTDIR = File.join(CWD,"public")
SPHINXDIR = File.join(CWD,"docs/Sphinx")
SYMESRC = File.join(CWD,"projects/symengine/symengine")
DOXXML = File.join(CWD,"docs/Doxygen/gen_docs/xml")
DOCCOV = File.join(OUTDIR,"doc-coverage.info")
# Where the genhtml files go
OUTCOV = File.join(OUTDIR,"doc_coverage")

# Exception
class RunnerException < StandardError
  def initialize(msg="Undefined runner, supports nix and system (with conda)", exception_type="custom")
    @exception_type = exception_type
    super(msg)
  end
end

class ExecException < StandardError
  def initialize(msg="Missing an application, typically doxyrest", exception_type="custom")
    @exception_type = exception_type
    super(msg)
  end
end

# Tasks
task :default => :darkServe

desc "Clean the generated content"
task :clean do
  rm_rf "public"
  rm_rf "docs/Doxygen/gen_docs"
  rm_rf "docs/Sphinx/build"
end

desc "Serve site with darkhttpd"
task :darkServe, [:port, :runner] do |task, args|
  args.with_defaults(:port => "1337", :runner => "system")
  if args.runner == "system" then
    sh "darkhttpd #{OUTDIR} --port #{args.port}"
  elsif args.runner == "nix" then
    sh "nix-shell #{NIXSHELL} --run 'darkhttpd #{OUTDIR} --port #{args.port}'"
  else
    raise RunnerException.new
  end
end

desc "Build full site documentation"
task :mkDocs, [:builder, :runner] do |taks, args| 
  args.with_defaults(:builder => "html", :port => "1337", :runner => "system")
  task(:mkSphinx).invoke(args.builder, args.runner)
  # task(:darkServe).invoke(args.port)
end

desc "Build doxygen"
task :mkDoxy, [:runner] do |task, args| 
  args.with_defaults(:runner => "system")
  Dir.chdir(to = File.join(CWD,"docs/Doxygen"))
  if ENV['dev']=="True" then
    puts "Skipping doxygen API generation as dev is \"True\""
  else
    if args.runner == "system" then
      system('doxygen', DOXYFILE)
    elsif args.runner == "nix" then
      sh "nix-shell #{NIXSHELL} --run 'doxygen #{DOXYFILE}'"
    else
      raise RunnerException.new
    end
  end
end

desc "Build doxyrest"
task :mkDoxyRest, [:builder, :runner] => "mkDoxy" do |task, args|
  args.with_defaults(:builder => "html", :runner => "system")
  Dir.chdir(to = CWD)
  if ENV['dev']=="True" then
    puts "Skipping doxyrest API generation as dev is \"True\""
  else
    if args.runner == "system" then
      if find_executable 'doxyrest' then
        sh "doxyrest -c ./docs/doxyrestConf.lua"
      elsif find_executable 'nix' then
        begin
          puts "System has no doxyrest, trying nix"
          sh "nix-shell #{NIXSHELL} --run 'doxyrest -c #{CWD}/docs/doxyrestConf.lua'"
        rescue
          puts "Falling back to conda"
          sh "conda run doxyrest -c #{CWD}/docs/doxyrestConf.lua"
        end
      else
        raise ExecException.new
      end
    elsif args.runner == "nix" then
      begin
        puts "System has no doxyrest, trying nix"
        sh "nix-shell #{NIXSHELL} --run 'doxyrest -c #{CWD}/docs/doxyrestConf.lua'"
      rescue
        puts "Falling back to conda"
        sh "conda run doxyrest -c #{CWD}/docs/doxyrestConf.lua"
      end
    else
      raise RunnerException.new
    end
  end
end

desc "Build Sphinx"
task :mkSphinx, [:builder, :runner] => ["mkDoxyRest"] do |task, args|
  args.with_defaults(:builder => "html", :runner => "system")
  Dir.chdir(to = SPHINXDIR)
  if args.runner == "system" then
    begin
      sh "conda env create -f #{CWD}/symedocs.yml"
    rescue
      sh "conda env update -f #{CWD}/symedocs.yml"
    end
    sh "conda run sphinx-build source #{OUTDIR} -b #{args.builder}"
  elsif args.runner == "nix" then
    begin
      sh "nix-shell #{NIXSHELL} --run 'sphinx-build source #{OUTDIR} -b #{args.builder}'"
    rescue
      puts "Handling the case where nix errors out by rescuing with conda"
      begin
        sh "conda env create -f #{CWD}/symedocs.yml"
      rescue
        sh "conda env update -f #{CWD}/symedocs.yml"
      end
      sh "conda run sphinx-build source #{OUTDIR} -b #{args.builder}"
    end 
  else
    raise RunnerException.new
  end
end

desc "Build API Coverage"
task :mkDocCover, [:runner] => ["mkDoxy"] do |task, args|
  args.with_defaults(:runner => "system")
  if args.runner == "system" then
    begin
      sh "conda env create -f #{CWD}/symedocs.yml"
    rescue
      sh "conda env update -f #{CWD}/symedocs.yml"
    end
    sh "conda run python3 -m coverxygen --xml-dir #{DOXXML} --src-dir #{SYMESRC} --output #{DOCCOV}"
  elsif args.runner == "nix" then
    sh "nix-shell #{NIXSHELL} --run 'python3 -m coverxygen --xml-dir #{DOXXML} --src-dir #{SYMESRC} --output #{DOCCOV}'"
  else
    raise RunnerException.new
  end
end

desc "Build HTML Coverage Report"
task :mkDocCovHTML, [:runner] => ["mkDocCover"] do |t, args| 
  args.with_defaults(:runner => "system")
  if args.runner == "system" then
    sh "genhtml --no-function-coverage --no-branch-coverage #{DOCCOV} -o #{OUTCOV}"
  elsif args.runner == "nix" then
    sh "nix-shell #{NIXSHELL} --run 'genhtml --no-function-coverage --no-branch-coverage #{DOCCOV} -o #{OUTCOV}'"
  else
    raise RunnerException.new
  end
end
