#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import datetime
import argparse

from biblat_process.utils import settings, cformatter

cformatter = cformatter()


class dumper():
    host = "aleph@{}"
    date = datetime.date.today().strftime('%d%m%y')

    def __init__(self, test_config=None):
        self.config = test_config or settings.get(u'app:main', {})
        self.config['local_path'] = self.config['local_path']

    def list_claper(self, base):
        print('listclaperexecute')
        lsqlScript = """
set source_par = '{dlib}'
source ${{alephm_proc}}/set_lib_env
setenv PATH /exlibris/aleph/.local/bin:$PATH
set dir='{remote_path}'
set fentrada=sis{dlib}_{fecha}.lst
cd $dir
cat <<EOF > consulta.sql
SET HEADING ON
SET LINESIZE 14
SET ECHO OFF
SET FEEDBACK OFF
SET PAUSE OFF
SET NEWPAGE 0
SET SPACE 0
SET PAGESIZE 0
SET TERMOUT OFF
SET VERIFY OFF
SPOOL $alephe_scratch/$fentrada
SELECT substr(z13u_rec_key,1,9)||'{dlib!u}'
FROM {dlib!u}.z13u
WHERE z13u_user_defined_3_code is NULL
ORDER BY substr(z13u_rec_key,1,9);
SPOOL OFF
EXIT
EOF
sqlplus {dlib}/{dlib} @consulta.sql
exit
"""
        remote_path = self.config['remote_path']
        remote_addr = self.config['remote_addr']
        if base == 'per01':
            lsqlScript += "\ngsed -r -i.bak -e '/^000200053/d' " \
                          "$alephe_scratch/$fentrada"
            lsqlScript += "\nrm $alephe_scratch/$fentrada.bak"
        lsqlScript = cformatter.format(lsqlScript, dlib=base,
                                       remote_path=remote_path,
                                       fecha=self.date)

        host = self.host.format(remote_addr)

        ssh = subprocess.Popen(["ssh", host, "csh -s"],
                               shell=False,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

        ssh.communicate(lsqlScript.encode())
        ssh.wait()

    def dump_claper(self, base):

        self.list_claper(base)
        print('dumpclaperexecute')
        script = """
set source_par = '{dlib}'
source ${{alephm_proc}}/set_lib_env
setenv PATH /exlibris/aleph/.local/bin:$PATH
set dir='{remote_path}'
set fentrada=sis{dlib}_{fecha}.lst
set fsalida={dlib}json_{fecha}.txt
cd $dir
rm -rf $fsalida
cd $aleph_proc
csh -f p_print_03 {dlib!u},$fentrada,ALL,,,,,,,,$fsalida,A,,,,N
mv $data_scratch/$fsalida $dir
while ( ! -e $dir/$fsalida )
    echo "no existe $fsalida"
    sleep 1
end
echo "EOF" >> $dir/$fsalida
echo `wc -l $alephe_scratch/$fentrada | awk '{{print $1}}'` >> $dir/$fsalida
cd $dir
gzip -9 $fsalida
            """
        remote_path = self.config['remote_path']
        remote_addr = self.config['remote_addr']
        lscript = cformatter.format(script, dlib=base,
                                    remote_path=remote_path, fecha=self.date)
        host = self.host.format(remote_addr)

        ssh = subprocess.Popen(["ssh", host, "csh -s"],
                               shell=False,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        ssh.communicate(lscript.encode())
        ssh.wait()

        self.pull_claper(base)

    def pull_claper(self, base):
        print('pullclaperexecute')
        local_path = self.config['local_path']
        remote_path = self.config['remote_path']
        remote_addr = self.config['remote_addr']
        cmd = "cat {remote_path}/{dlib}json_{fecha}.txt.gz" \
            .format(remote_path=remote_path, dlib=base, fecha=self.date)
        output_file = open('{local_path}/{dlib}_valid.txt.gz'.format(
            local_path=local_path, dlib=base), 'w')

        host = self.host.format(remote_addr)

        ssh = subprocess.Popen(["ssh",
                                host, cmd],
                               shell=False,
                               stdout=output_file)
        ssh.wait()
        output_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cosecha de archivos"
    )

    parser.add_argument(
        '--periodica',
        action='store_true',
        dest='periodica',
        help='Procesando periodica'
    )

    parser.add_argument(
        '--all',

        action='store_true',
        dest='all',
        help='Procesando periodica y clase'
    )

    parser.add_argument(
        '--clase',
        action='store_true',
        dest='clase',
        help='Procesando clase'
    )
    args = parser.parse_args()

    d = dumper()

    if args.periodica:

        d.dump_claper('per01')

    elif args.clase:

        d.dump_claper('cla01')
    else:
        d.dump_claper('cla01')
        d.dump_claper('per01')