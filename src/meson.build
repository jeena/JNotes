pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'jnotes'
gnome = import('gnome')

gnome.compile_resources('jnotes',
  'jnotes.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'jnotes.in',
  output: 'jnotes',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

jnotes_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'preferences.py',
  'gsettings.py',
  'sync.py',
  'sidebar.py',
  'notes_list.py',
]

install_data(jnotes_sources, install_dir: moduledir)
