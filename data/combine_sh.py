import os 
from info import common

normlized_common = set()



def main():
    for tic in common:
        normlized_common.add('{:016d}'.format(tic))

    outname = "./all_light_curve.sh"
    with open(outname, 'w') as out:
        for sub in os.listdir("./scripts"):
            fname = os.path.join('./scripts', sub)
            with open(fname) as f:
                for line in f:
                    line = line.strip()
                    if line == '':
                        continue
                    try:
                        target = line.split()[5]
                        if target.split('-')[2] in normlized_common:
                            out.write(line.split()[-1] + '\n')
                    except:
                        continue

main()
