from argparse import ArgumentParser
import csv
from os.path import join

from quid.helper.Loader import load_citation_sources


def read_tokens(token_file_path):
    result = []

    with open(token_file_path, 'r', encoding='utf-8') as token_file:
        reader = csv.reader(token_file, delimiter='\t')

        next(reader, None)

        for row in reader:
            if len(row) == 1:
                result.append((row[0]))
            elif len(row) == 4:
                result.append((row[0], row[1], int(row[2]), int(row[3])))
            else:
                raise Exception("Invalid length")

    return result


def read_passages(passages_file_path):
    return load_citation_sources(passages_file_path)


def update_tokens(tokens, passages):
    result = []

    for token in tokens:
        found = False

        if isinstance(token, str):
            result.append(token)
            found = True
        else:
            tstart = token[2]
            tend = token[3]
            for passage in passages:
                for source_segment in passage.source_segments:
                    if tstart >= source_segment.start and tend <= source_segment.end:
                        result.append((token[0], token[1], token[2], token[3], source_segment.my_id,
                                       source_segment.token_length, source_segment.frequency))
                        found = True
                        break

                if found:
                    break

        if not found:
            result.append((token[0], token[1], token[2], token[3], -1, 0, 0))

    return result


def main():
    argument_parser = ArgumentParser()

    argument_parser.add_argument("tokens_file_path", nargs=1, metavar="tokens-file-path",
                                 help="Path to the tokens tsv file")
    argument_parser.add_argument("passages_file_path", nargs=1, metavar="passages-file-path",
                                 help="Path to the passages json file")
    argument_parser.add_argument("output_folder_path", nargs=1, metavar="output-folder-path",
                                 help="Path to the output folder")

    args = argument_parser.parse_args()

    tokens_file_path = args.tokens_file_path[0]
    passages_file_path = args.passages_file_path[0]
    output_folder_path = args.output_folder_path[0]

    tokens = read_tokens(tokens_file_path)
    passages = read_passages(passages_file_path)

    updated_tokens = update_tokens(tokens, passages)

    with open(join(output_folder_path, "keypassages.tsv"), "wt", encoding="utf-8") as out_file:
        writer = csv.writer(out_file, delimiter="\t", lineterminator="\n")
        writer.writerow(["id", "token", "start", "end", "segment", "length", "citations"])
        for token in updated_tokens:
            if isinstance(token, str):
                writer.writerow([token])
            else:
                writer.writerow(token)


if __name__ == '__main__':
    main()
