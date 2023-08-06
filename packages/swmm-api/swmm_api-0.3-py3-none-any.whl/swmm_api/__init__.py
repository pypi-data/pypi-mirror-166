from .input_file import read_inp_file, SwmmInput
from .report_file import read_rpt_file, SwmmReport
from .output_file import read_out_file, SwmmOutput, out2frame
from .run import swmm5_run
from .hotstart import SwmmHotstart

# https://peps.python.org/pep-0440/
# Pre-release segment: {a|b|rc}N
# Post-release segment: .postN oder .rN oder .revN
# Development release segment: .devN
# anstatt . kann auch - oder _ verwendet werden
__version__ = '0.3'
