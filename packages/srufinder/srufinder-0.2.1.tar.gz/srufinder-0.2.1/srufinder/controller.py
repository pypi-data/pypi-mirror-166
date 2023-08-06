import os
import logging
import sys
import pkg_resources
import glob

import pandas as pd

from Bio import SeqIO

class Controller(object):

    def __init__(self, args):
        '''
        Initialize master object by:
        Getting arguments from input
        Starting the logger
        Checking database, input, and output
        Write the arguments to a file
        '''

        self.fasta = args.input
        self.out = args.output
        self.prod = args.prodigal
        self.db = args.db
        self.threads = args.threads
        self.orf = args.orf
        self.log_lvl = args.log_lvl
        self.word_size = args.word_size
        self.identity = args.identity
        self.max_dist = args.max_dist
        self.coverage = args.coverage
        self.score = args.score
        self.coverage_part = args.coverage_part
        self.flank = args.flank
        self.spacer_identity = args.spacer_identity
        self.spacer_coverage = args.spacer_coverage
        self.selfmatch = args.selfmatch
        self.in_orf = args.in_orf

        # Logger
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=self.log_lvl)
        logging.info('Running SRUFinder version {}'.format(pkg_resources.require("srufinder")[0].version))

        # Force consistency
        self.out = os.path.join(self.out, '')

        # Check databases
        self.check_db()
        
        # Check input and output
        self.load_input()
        self.check_out()

        # Get repeat lengths
        self.get_len()

        # Write arguments
        da = vars(args)
        f = open(self.out+'arguments.tab', 'w')
        for k, v in da.items():
            f.write('{}: {}\n'.format(k, v))
        f.close()

    def check_out(self):
        '''
        Create the output dir if possible else terminate
        '''

        try:
            os.mkdir(self.out)
        except FileExistsError:
            logging.error('Directory '+self.out+' already exists')
            sys.exit()

    def load_input(self):
        '''
        Check that input file exists and that it looks like a fasta
        '''

        if os.path.isfile(self.fasta):
            try:
                self.sequences = {}
                with open(self.fasta, 'r') as handle:
                    for rec in SeqIO.parse(handle, 'fasta'):
                        if rec.id in self.sequences:
                            logging.error('Duplicate fasta headers detected!\nPlease ensure input has unique headers without spaces.')
                            sys.exit()
                        self.sequences[rec.id] = rec.seq

            except:
                logging.error('Input file is in bad format')
                sys.exit()
        else:
            logging.error('Could not find input file')
            sys.exit()

    def check_db(self):
        '''
        Ensure that the database environment variable is set
        if not database is explicilitly given
        '''

        if self.db == '':
            try:
                self.db = os.environ['SRUFINDER_DB']
            except:
                logging.error('Could not find database directory')
                sys.exit()

        self.repeatdb = os.path.join(self.db, "repeats.fa")

    def get_len(self):
        '''
        Get lengths of all repeat sequences for coverage calculation later
        '''

        with open(self.repeatdb, 'r') as handle:
            fas = SeqIO.parse(handle, 'fasta')
            len_dict = {}
            for fa in fas:
                len_dict[str(fa.id)] = len(fa.seq)

        self.len_df = pd.DataFrame.from_dict(len_dict, orient='index', columns=['Repeat_len']) 

    def clean(self):
        '''
        Removing temporary files
        '''

        logging.debug('Removing temporary files')

        if os.path.isfile(self.out+'masked.fna'):
            list(map(os.remove, glob.glob(self.out+'masked*')))
        
        if os.path.isfile(self.out+'genome.fna'):
            list(map(os.remove, glob.glob(self.out+'genome*')))

        if os.path.isfile(self.out+'flanking.fna'):
            os.remove(self.out+'flanking.fna')
        
        os.remove(self.out+'prodigal.gff')
