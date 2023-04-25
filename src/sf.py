import stockfish
import chess

sf = stockfish.Stockfish(r'C:\Users\Rushdeep Dinda\Downloads\stockfish_15.1_win_x64_avx2\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2')
sf.set_depth(20)
sf.set_skill_level(20)
sf.set_elo_rating(1600)
# print(sf.get_parameters())
