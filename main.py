import sys
import re
import click
from path import Path
from Bio import PDB
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

sys.stdout.reconfigure(encoding='utf-8')

@click.command(help='PDBonnie: a simple PDB structures downloader for bioinformatics research.')
@click.argument('pdb_id', type=str)
@click.option('--format', '-f', type=str, default='mmcif', help='Format of downloaded file (mmcif, pdb, xml, mmtf, bundle), mmcif by default.')
@click.option('--output', '-o', type=str, default='.', help='Path where to save file, current by default.')
@click.option('--obsolete', is_flag=True, default=False, help='Enable downloading obsolete structures.')

def main(pdb_id: str, format: str, output: str, obsolete: bool):
    start_time = perf_counter()

    # PDB ID 校验：去除空格、转大写、正则验证4位字母数字
    pdb_id = pdb_id.strip().upper()
    if not re.fullmatch(r'[A-Z0-9]{4}', pdb_id):
        print(f'Error: Invalid PDB ID "{pdb_id}". Expected 4 alphanumeric characters (e.g. 3COM).')
        sys.exit(1)
    
    pdbl = PDB.PDBList()

    file_format_dict = {
        'pdb': 'pdb',
        'mmcif': 'mmCif',
        'xml': 'xml',
        'mmtf': 'mmtf',
        'bundle': 'bundle'
    }
    target_format: str = file_format_dict.get(format)
    if target_format is None:
        print(f"Error: Invalid format: {format}")
        sys.exit(1)
    try:
        # 在独立线程中执行下载，限制 30 秒超时
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                pdbl.retrieve_pdb_file,
                pdb_id,
                pdir=Path(output).absolute(),
                file_format=target_format,
                overwrite=True,
                obsolete=obsolete,
            )
            file_path = future.result(timeout=30)
        end_time = perf_counter()
        print(f'Download completed in {round((end_time - start_time), 2)} s.')
        print(f'Structure saved in {file_path}')
    except FutureTimeoutError:
        print(f'Error: Download timed out after 30 seconds.')
        sys.exit(1)
    except Exception as e:
        print(f'Error: Failed to download structure ({e})')
        sys.exit(1)

if __name__ == '__main__':
    main()

