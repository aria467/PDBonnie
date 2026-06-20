import sys
import os
import re
import logging
import click
from path import Path
from Bio import PDB
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError, as_completed

sys.stdout.reconfigure(encoding='utf-8')

def _retrieve_quiet(pdbl, pdb_id, pdir, file_format, overwrite, obsolete):
    """下载 PDB 文件。"""
    return pdbl.retrieve_pdb_file(
        pdb_id, pdir=pdir, file_format=file_format,
        overwrite=overwrite, obsolete=obsolete,
    )


@click.command(help='PDBonnie: a simple PDB structures downloader for bioinformatics research.')
@click.argument('pdb_ids', type=str, nargs=-1)
@click.option('--format', '-f', type=str, default='mmcif', help='Format of downloaded file (mmcif, pdb, xml, mmtf, bundle), mmcif by default.')
@click.option('--path', '-p', type=str, default='.', help='Path where to save file, `.` by default.')
@click.option('--obsolete', is_flag=True, default=False, help='Using to enable downloading obsolete structures.')
@click.option('--threads', '-t', type=int, default=1, help='Threads that being used in downloading.')

def main(pdb_ids: tuple[str, ...], format: str, path: str, obsolete: bool, threads: int):

    # PDB ID 校验：去除空格、转大写、正则验证4位字母数字
    if not pdb_ids:
        print('Error: At least one PDB ID is required.\nUsage: main.py [OPTIONS] PDB_IDS...')
        sys.exit(1)

    pdb_ids = tuple(pdb_id.strip().upper() for pdb_id in pdb_ids)
    invalid_pdb_ids = [pid for pid in pdb_ids if not re.fullmatch(r'[A-Z0-9]{4}', pid)]
    if invalid_pdb_ids:
        print(f'Error: Invalid PDB ID "{invalid_pdb_ids}".\nExpected 4 alphanumeric characters.')
        sys.exit(1)
    
    
    pdbl = PDB.PDBList()
    pdbl._verbose = False

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
        start_time = perf_counter()
        total = len(pdb_ids)

        # --- ANSI 终端控制常量 ---
        GRAY  = '\033[90m'
        GREEN = '\033[32m'
        RED   = '\033[31m'
        RESET = '\033[0m'

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {}
            for pid in pdb_ids:
                future = executor.submit(
                    _retrieve_quiet,
                    pdbl, pid, Path(path).absolute(), target_format,
                    True, obsolete,
                )
                futures[future] = pid

            completed = 0
            failed = 0
            for future in as_completed(futures):
                pid = futures[future]
                try:
                    file_path = Path(future.result(timeout=30))
                except Exception:
                    failed += 1
                    print(f'{RED}[{completed + failed}/{total}] {pid} download failed{RESET}')
                    continue

                # rename
                new_path = file_path.parent.joinpath(f'{pid.lower()}{file_path.suffix}')
                if new_path.suffix == '.ent':
                    new_path = Path(path).absolute().joinpath(f'{pid.upper()}.pdb')
                os.rename(file_path, new_path)

                completed += 1
                print(f'{GRAY}[{completed}/{total}] {GREEN}✓ {pid} → {new_path.name}{RESET}')

        # 打印下载目录
        download_dir = Path(path).absolute()
        print(f'\n{GRAY}Download directory: {download_dir}{RESET}')

        # 下载完成，换行打印汇总
        status_color = GREEN if completed == total else RED
        total_elapsed = round(perf_counter() - start_time, 2)
        print(f'{status_color}{completed}/{total} structures downloaded in {total_elapsed} s.{RESET}')
        if failed:
            print(f'{RED}{failed} failed.{RESET}')

    except FutureTimeoutError:
        print(f'\n{RED}Error: Download timed out after 30 seconds.{RESET}')
        sys.exit(1)
    except Exception as e:
        print(f'\n{RED}Error: {e}{RESET}')
        sys.exit(1)
if __name__ == '__main__':
    main()