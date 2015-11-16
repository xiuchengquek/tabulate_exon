__author__ = 'xiuchengquek'





import unittest
from tabulate_exon_coverage import Transcript, transcriptManager


class testTranscript(unittest.TestCase):



    def test_create_transcript(self):
        transcript_a = Transcript('transcriptA')
        self.assertEqual(transcript_a.id, 'transcriptA')
        self.assertEqual(transcript_a.coverage_base, 0)
        self.assertEqual(transcript_a.length, 0)

    def test_add_covereage(self):
        transcript_a = Transcript('transcriptA')
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(0)

        self.assertEqual(transcript_a.bases, 30)
        self.assertEqual(transcript_a.coverage_base, 3)
        self.assertEqual(transcript_a.length, 4)




    def test_filter(self):
        transcript_a = Transcript('transcriptA')
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(10)
        transcript_a.add_coverage(0)

        self.assertEqual(transcript_a.bases, 30)
        self.assertEqual(transcript_a.coverage_base, 3)
        self.assertEqual(transcript_a.length, 4)
        self.assertFalse(transcript_a.filter(1, 10))
        self.assertFalse(transcript_a.filter(0.5, 100))
        self.assertTrue(transcript_a.filter(0.5, 5))


class testTranscriptManager(unittest.TestCase):

    def setUp(self):
        transcript_manager = transcriptManager()
        transcript_manager.add_coverage('transcriptA', 10)
        transcript_manager.add_coverage('transcriptA', 10)
        transcript_manager.add_coverage('transcriptA', 10)
        transcript_manager.add_coverage('transcriptA', 0)

        transcript_manager.add_coverage('transcriptB', 100)
        transcript_manager.add_coverage('transcriptB', 100)
        transcript_manager.add_coverage('transcriptB', 100)
        transcript_manager.add_coverage('transcriptB', 100)
        transcript_manager.add_coverage('transcriptB', 0)

        transcript_manager.save()

        self.transcript_manager = transcript_manager

    def test_both_transcript_present(self):

        transcript_manager = self.transcript_manager
        transcriptA = transcript_manager.get_transcript_by_id('transcriptA')
        transcriptB = transcript_manager.get_transcript_by_id('transcriptB')

        self.assertEqual(transcriptA.id, 'transcriptA')
        self.assertEqual(transcriptB.id, 'transcriptB')

    def test_add_coverage(self):
        transcript_manager = self.transcript_manager
        transcriptA = transcript_manager.get_transcript_by_id('transcriptA')
        transcriptB = transcript_manager.get_transcript_by_id('transcriptB')

        self.assertEqual(transcriptA.coverage_base, 3)
        self.assertEqual(transcriptA.bases, 30)
        self.assertEqual(transcriptA.length, 4)

        self.assertEqual(transcriptB.coverage_base, 4)
        self.assertEqual(transcriptB.bases, 400)
        self.assertEqual(transcriptB.length, 5)

        transcript_manager.add_coverage('transcriptC', 10)
        transcript_manager.save()

    def test_filter_transcript(self):
        transcript_manager = self.transcript_manager
        filtered_transcripts = transcript_manager.filter_transcript(0.2, 10)
        line = 'transcriptA\t30\t4\t3\n'

        self.assertEqual(filtered_transcripts.next(), line)

        line = 'transcriptB\t400\t5\t4\n'
        self.assertEqual(filtered_transcripts.next(), line)

















if __name__ == '__main__':
    unittest.main()




