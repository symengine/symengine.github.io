require 'rake'

# Variables
CWD = File.expand_path(__dir__)
DOXYFILE = "Doxyfile-syme.cfg"
OUTDIR = File.join(CWD,"public")
SPHINXDIR = File.join(CWD,"docs/Sphinx")
SYMESRC = File.join(CWD,"projects/symengine/symengine")
DOXXML = File.join(CWD,"docs/Doxygen/gen_docs/xml")
DOCCOV = File.join(OUTDIR,"doc-coverage.info")
# Where the genhtml files go
OUTCOV = File.join(OUTDIR,"doc_coverage")

# Tasks
task :default => :darkServe

desc "Clean the generated content"
task :clean do
  rm_rf "public"
  rm_rf "docs/Doxygen/gen_docs"
  rm_rf "docs/Sphinx/build"
end

desc "Serve site with darkhttpd"
task :darkServe, [:port] do |task, args|
  args.with_defaults(:port => "1337")
  sh "darkhttpd #{OUTDIR} --port #{args.port}"
end

desc "Build Nix Sphinx, use as nix-shell --run 'rake mkNixDoc' --pure"
task :mkNixDoc, [:builder] => "mkDoxy" do |task, args|
  args.with_defaults(:builder => "html")
  Dir.chdir(to = SPHINXDIR)
  sh "sphinx-build source #{OUTDIR} -b #{args.builder}"
end

desc "Build site without Nix"
task :noNixBuild => "mkSphinx" do
  Rake::Task["darkServe"].execute
end

desc "Build doxygen"
task :mkDoxy do
  Dir.chdir(to = File.join(CWD,"docs/Doxygen"))
  system('doxygen', DOXYFILE)
end

desc "Build doxyrest"
task :mkDoxyRest, [:builder] => "mkDoxy" do |task, args|
  args.with_defaults(:builder => "html")
  Dir.chdir(to = CWD)
  sh "nix-shell #{File.join(CWD,"shell.nix")} --run 'doxyrest -c ./docs/doxyrestConf.lua'"
end

desc "Build Sphinx"
task :mkSphinx, [:builder] => ["mkDoxyRest"] do |task, args|
  args.with_defaults(:builder => "html")
  Dir.chdir(to = File.join(CWD,"docs/Sphinx"))
  sh "poetry install"
  sh "poetry run sphinx-build source #{OUTDIR} -b #{args.builder}"
end

desc "Build API Coverage"
task :mkDocCover, [:runner] => ["mkDoxy"] do |task, args|
  args.with_defaults(:runner => "poetry")
  if :runner == "nix"
    sh "python3 -m coverxygen --xml-dir #{DOXXML} --src-dir #{SYMESRC} --output #{DOCCOV}"
  else
    sh "poetry install"
    sh "poetry run python3 -m coverxygen --xml-dir #{DOXXML} --src-dir #{SYMESRC} --output #{DOCCOV}"
  end
end

desc "Build HTML Coverage Report"
task :mkDocCovHTML => ["mkDocCover"] do
  sh "genhtml --no-function-coverage --no-branch-coverage #{DOCCOV} -o #{OUTCOV}"
end
