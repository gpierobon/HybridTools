import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
        '-k',
        "--key",
        dest="key",
        help="Choose key",
        type=str,
        required=True
        )


parser.add_argument(
        '-ot',
        "--otype",
        dest="otype",
        help="Choose option type: (0=Start, 1=Restart, 2=Post)",
        type=int,
        required=True
        )

parser.add_argument(
        '-c',
        "--class_file",
        dest="fclass",
        help="Class file for Input/Output",
        type=str,
        required=False
        )
        
parser.add_argument(
        '-m',
        "--muflr_file",
        dest="fmflr",
        help="MuFLR file for Input/Output",
        type=str,
        required=False
        )

parser.add_argument(
        '-sf',
        "--sim_folder",
        dest="simfol",
        help="Path of simulation folder",
        type=str,
        required=False
        )


parser.add_argument(
        '-pf',
        "--print_muflr",
        dest="pr_flag",
        help="Print flag for MuFLR (see Amol's code)",
        type=int,
        required=False
        )

parser.add_argument(
        '-zi',
        "--mf_zi",
        dest="zi",
        help="Initial redshift for MuFLR",
        type=float,
        required=False
        )

parser.add_argument(
        '-zf',
        "--mf_zf",
        dest="zf",
        help="Final redshift for MuFLR (Nbody initial time)",
        type=float,
        required=False
        )


parser.add_argument(
        '-pk',
        "--out_pk",
        dest="out_pk",
        help="Name of PowerSpectrumFile in param file",
        type=str,
        required=False
        )

parser.add_argument(
        '-gr',
        "--out_gr",
        dest="out_gr",
        help="Name of GrowthRateFile in param file",
        type=str,
        required=False
        )

parser.add_argument(
        '-cb',
        "--out_cb",
        dest="out_cb",
        help="Name of CBPowerSpectrumFile in param file",
        type=str,
        required=False
        )


parser.add_argument(
        '-pp',
        "--pp_index",
        dest="pp_index",
        help="Post-processing option",
        type=int,
        required=False
        )

parser.add_argument(
        '-sa',
        "--snap_num",
        dest="snap_num",
        help="Snapshot number to analyse",
        type=int,
        required=False
        )

parser.add_argument(
        '-id',
        "--input_delta",
        dest="in_de",
        help="Neutrino stream delta",
        type=str,
        required=False
        )


parser.add_argument(
        '-it',
        "--input_theta",
        dest="in_th",
        help="Neutrino stream theta",
        type=str,
        required=False
        )

parser.add_argument(
        '-icb',
        "--input_cb",
        dest="in_cb",
        help="Total particle power spectrum",
        type=str,
        required=False
        )


parser.add_argument(
        '-str',
        "--stream",
        dest="stream",
        help="Neutrino stream",
        type=int,
        required=False
        )

parser.add_argument(
        '-Ns',
        "--Nstreams",
        dest="Nstreams",
        help="Number of streams",
        type=int,
        required=False
        )


