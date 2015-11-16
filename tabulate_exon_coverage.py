__author__ = 'xiuchengquek'







import sys
import argparse
import re



class Transcript:

    def __init__(self, id):
        self.id = id
        self.coverage_base = 0
        self.bases = 0
        self.length = 0


    def add_coverage(self, bases):
        self.length += 1
        if int(bases) != 0:
            self.coverage_base += 1

        self.bases += bases

    def filter(self, coverage_cutoff, depth_cutoff):
        coverage_exon = float(self.coverage_base) / float(self.length)

        try :
            depth  = float(self.bases) / float(self.coverage_base)
        except ZeroDivisionError:
            depth = 0
        if (coverage_exon >= coverage_cutoff ) and (depth >= depth_cutoff):
            return True
        else:
            return False

class transcriptManager:

    def __init__(self):
        self.transcript_dict = {}
        self.current_transcript = None

    def __get_transcript_or_create__(self, transcript_id):
        transcript_obj = self.transcript_dict.get(transcript_id, None)
        if transcript_obj is None:
            transcript_obj = Transcript(transcript_id)
        return transcript_obj

    def add_coverage(self, transcript_id, bases):

        if self.current_transcript is None:
            self.current_transcript = Transcript(transcript_id)

        ## save transcript
        if self.current_transcript.id != transcript_id:
            self.save()
            ## create new instance
            self.current_transcript = Transcript(transcript_id)

        self.current_transcript.add_coverage(bases)

    def save(self):
        self.transcript_dict[self.current_transcript.id] = self.current_transcript


    def __str__(self):
        retr_str = []
        for transcript_id, transcript_obj in self.transcript_dict.items():
            line = "%s\t%i\t%i\t%i" % (transcript_id, transcript_obj.bases, transcript_obj.length, transcript_obj.coverage_base)
            retr_str.append(line)

        return "\n".join(retr_str)


    def filter_transcript(self, coverage, counts):
        for transcript_id, transcript_obj in self.transcript_dict.items():
            if transcript_obj.filter(float(coverage), int(counts)):
                line =  "%s\t%i\t%i\t%i" % (transcript_id, transcript_obj.bases, transcript_obj.length, transcript_obj.coverage_base)
                yield line






    def get_transcript_by_id(self, transcript_id):
        return self.transcript_dict.get(transcript_id, None)





if __name__ == '__main__' :

    parser = argparse.ArgumentParser(description='Coverage file')
    parser.add_argument('--coverage', help = 'coverage file ')
    parser.add_argument('--cov_cutoff', help = 'coverage file ', type=float)
    parser.add_argument('--depth', help = 'coverage file ', type=int)

    parser.add_argument('--output', help = 'coverage file ')

    args = parser.parse_args()
    coverage_file = args.coverage
    output_file = args.output
    transcript_re = re.compile('transcript_id \"([\w]+)\.')
    transcript_dict = {}

    cov_cutoff = args.cov_cutoff
    depth = args.depth

    transcript_manager = transcriptManager()

    with open(coverage_file, 'r') as f:
        for line in f:
            line = line.strip()
            fields = line.split('\t')
            transcript_id = transcript_re.search(fields[9]).group(1)
            print(transcript_id)
            transcript_manager.add_coverage(transcript_id, bases=int(fields[-1]))


    with open(output_file, 'w+') as f:
        for x in transcript_manager.filter_transcript(cov_cutoff, depth):
            f.write("%s\n" % x)














































