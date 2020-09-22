require 'rake'

# Variables
CWD = File.expand_path(__dir__)
DOXYFILE = "Doxyfile-syme.cfg"
OUTDIR = File.join(CWD,"public")

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
task :mkNixDoc => "mkDoxy" do
  Dir.chdir(to = File.join(CWD,"docs/Sphinx"))
  sh "sphinx-build source #{OUTDIR}"
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

desc "Build Sphinx"
task :mkSphinx => "mkDoxy" do
  Dir.chdir(to = File.join(CWD,"docs/Sphinx"))
  sh "poetry install"
  sh "poetry run sphinx-build source #{OUTDIR}"
end
