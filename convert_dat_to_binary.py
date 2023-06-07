# converter, from ordinary file to binary file.
import struct

# Usage example
input_file = "N3LO_EMN500_kmax8_N100_Jmax8-hrz.dat"
output_file = "N3LO_EMN500_kmax8_N100_Jmax8-hrz.bin"


def convert_dat_to_binary(input_file, output_file):
    with open(input_file, "r") as fp_in, open(output_file, "wb") as fp_out:
        lines = fp_in.readlines()

        # Parse and write NMesh, Jmax, and NChan to binary file
        NMesh = int(lines[1])
        Jmax = int(lines[3])
        NChan = int(lines[5])
        fp_out.write(struct.pack("<i", NMesh))
        fp_out.write(struct.pack("<i", Jmax))
        fp_out.write(struct.pack("<i", NChan))

        # Parse and write Momentum Mesh Points to binary file
        start_index = 7
        for i in range(NMesh):
            fp_out.write(struct.pack("<d", float(lines[start_index + i])))

        # Parse and write Momentum Mesh Weights to binary file
        start_index = start_index + NMesh + 1
        for i in range(NMesh):
            fp_out.write(struct.pack("<d", float(lines[start_index + i])))

        # Parse and write J, Prty, S, Tz, Ndim, and V values to binary file
        start_index = 2 * NMesh + 9
        for _ in range(NChan):
            J = int(lines[start_index])
            Prty = int(lines[start_index + 2])
            S = int(lines[start_index + 4])
            Tz = int(lines[start_index + 6])
            Ndim = int(lines[start_index + 8])
            fp_out.write(struct.pack("<i", J))
            fp_out.write(struct.pack("<i", Prty))
            fp_out.write(struct.pack("<i", S))
            fp_out.write(struct.pack("<i", Tz))
            fp_out.write(struct.pack("<i", Ndim))

            V_lines = lines[start_index + 10 : start_index + 10 + Ndim]
            V_values = [float(value) for line in V_lines for value in line.split()]
            for value in V_values:
                fp_out.write(struct.pack("<d", value))

            start_index += 11 + Ndim

    print(f"Conversion complete. The data has been saved to {output_file}.")


convert_dat_to_binary(input_file, output_file)
