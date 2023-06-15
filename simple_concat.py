from pathlib import Path

transcript_paths = Path('data','user_response').glob('*.txt')
simple_concat_path = Path('data','simple_concat.txt')

sc = ''
for tp in transcript_paths:
    sc += tp.read_text(encoding='utf-8') + '\n\n'

simple_concat_path.write_text(sc, encoding='utf-8')
print('Done')

