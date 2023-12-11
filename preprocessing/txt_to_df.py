import pandas as pd
import sys


def text_to_csv(input_file, output_file):
    df = pd.read_table(input_file, encoding = "utf-8", names=['keyword', 'count'])
    df_transpose = df.transpose()
    print(df_transpose)
    df_transpose = df_transpose.rename(columns=df_transpose.iloc[0])
    print(df_transpose)
    df_transpose = df_transpose.drop(df_transpose.index[0])
    df_transpose.to_csv(output_file, index=False)

if __name__ == "__main__":
    # 명령행에서 파일 이름을 인자로 받기
    if len(sys.argv) != 3:
        print("Usage: python script.py input.txt output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # 함수 호출
    text_to_csv(input_file, output_file)

    print(f"Conversion complete. CSV file saved as {output_file}")
