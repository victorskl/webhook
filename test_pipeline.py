import os, sys, logging, shlex, subprocess

SCRIPT = 'pipeline.sh'
pr_commit = sys.argv[1]

working_dir = os.path.dirname(os.path.realpath(__file__))
logging.debug('working_dir: ' + working_dir)
cmd = shlex.split('bash ' + SCRIPT + ' ' + pr_commit)
process = subprocess.Popen(cmd, cwd=working_dir, stdout=subprocess.PIPE)
for c in iter(lambda: process.stdout.read(1), ''):
    sys.stdout.write(c)
