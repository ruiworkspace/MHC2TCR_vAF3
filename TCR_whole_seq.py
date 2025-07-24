import csv

# Constants (replace these with your real sequences)
TRAV10N = "MKTSLHTVFLFLWLWMDWESHGEKVEQHESTLSVREGDSAVINCTYTDTASSYFPWYKQEAGKSLHFVIDIRSNVDRKQSQRLTVLLDKKAKRFSLHITATQPEDSAIYF"
TRAJ9 = "GTGTSLLVDP"
TCRAC = "NIQNPEPAVYQLKDPRSQDSTLCLFTDFDSQINVPKTMESGTFITDKTVLDMKAMDSKSNGAIAWSNQTSFTCQDIFKETNATYPSSDVPCDATLTEKSFETDMNLNFQNLSVMGLRILLLKVAGFNLLMTLRLWSS"
TRBV31 = "MLYSLLAFLLGMFLGVSAQTIHQWPVAEIKAVGSPLSLGCTIKGKSSPNLYWYWQATGGTLQQLFYSITVGQVESVVQLNLSASRPKDDQFILSTEKLLLSHSGFYL"
TRBJ2 = "GAGTRLSVL"
TCRBC = "EDLRNVTPPKVSLFEPSKAEIANKQKATLVCLARGFFPDHVELSWWVNGKEVHSGVSTDPQAYKESNYSYCLSSRLRVSATFWHNPRNHFRCQVQFHGLSEEDKWPEGSPKPVTQNISAEAWGRADCGITSASYHQGVLSATILYEILLGKATLYAVLVSGLVLMAMVKKKNS*"
linker = "GSGATNFSLLKQAGDVEENPGP"

# Input/output files
input_csv = "/home/rxu/MHC2TCR/test1_250723/prep/TCR_cdr3_strict_deduplicated.csv" # change this to your one directiory
output_file = "/home/rxu/MHC2TCR/test1_250723/prep/full_tcr_sequences.txt" # change this to your one directiory

with open(input_csv, newline='') as csvfile, open(output_file, "w") as outfile:
    reader = csv.reader(csvfile)
    
    for row in reader:
        if len(row) != 3:
            print(f"Skipping malformed row: {row}")
            continue
        
        name, cdr3a, cdr3b = [x.strip() for x in row]

        full_seq = (
            TRAV10N + cdr3a + TRAJ9 + TCRAC +
            linker +
            TRBV31 + cdr3b + TRBJ2 + TCRBC
        )

        outfile.write(f">{name}\n{full_seq}\n")

print(f"Full TCR sequences written to: {output_file}")
