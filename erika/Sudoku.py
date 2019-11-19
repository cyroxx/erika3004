def main():
    cells_x = 4
    blocks_x = 3
    horizontal_line = "\n" + "".join(["-".join(["+"] * cells_x)] * blocks_x) + "\n"
    number_row = "".join(["1".join(["|"] * cells_x)] * blocks_x)
    print(number_row.join([horizontal_line] * cells_x))


if __name__ == "__main__":
    main()
