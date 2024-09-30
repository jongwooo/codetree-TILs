import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static final int[][] dirs = { { -1, 0 }, { -1, 1 }, { 0, 1 }, { 1, 1 }, { 1, 0 }, { 1, -1 }, { 0, -1 },
			{ -1, -1 } }; // ↑, ↗, →, ↘, ↓, ↙, ←, ↖

	static int N, M, K;
	static Queue<Atom>[][] grid;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		K = Integer.parseInt(st.nextToken());
		grid = new Queue[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				grid[i][j] = new ArrayDeque<>();
			}
		}
		for (int i = 0; i < M; i++) {
			st = new StringTokenizer(br.readLine());
			final int x = Integer.parseInt(st.nextToken()) - 1;
			final int y = Integer.parseInt(st.nextToken()) - 1;
			final int m = Integer.parseInt(st.nextToken());
			final int s = Integer.parseInt(st.nextToken());
			final int d = Integer.parseInt(st.nextToken());
			grid[x][y].add(new Atom(m, s, d));
		}
		for (int i = 0; i < K; i++) {
			atomsMove();
			atomsSynthesis();
		}
		int result = 0;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				while (!grid[i][j].isEmpty()) {
					final Atom atom = grid[i][j].poll();
					result += atom.m;
				}
			}
		}
		System.out.println(result);
	}

	private static void atomsMove() {
		final Queue<Atom>[][] temp = new Queue[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				temp[i][j] = new ArrayDeque<>();
			}
		}
		for (int x = 0; x < N; x++) {
			for (int y = 0; y < N; y++) {
				while (!grid[x][y].isEmpty()) {
					final Atom atom = grid[x][y].poll();
					final int nx = convertPos(x + dirs[atom.d][0] * atom.s);
					final int ny = convertPos(y + dirs[atom.d][1] * atom.s);
					temp[nx][ny].add(atom);
				}
			}
		}
		grid = temp;
	}

	private static void atomsSynthesis() {
		final Queue<Atom>[][] temp = new Queue[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				temp[i][j] = new ArrayDeque<>();
			}
		}
		for (int x = 0; x < N; x++) {
			for (int y = 0; y < N; y++) {
				final int atomCount = grid[x][y].size();
				if (atomCount >= 2) {
					int mSum = 0;
					int sSum = 0;
					int udlr = 0;
					int diagonal = 0;
					while (!grid[x][y].isEmpty()) {
						final Atom atom = grid[x][y].poll();
						mSum += atom.m;
						sSum += atom.s;
						if (atom.d % 2 == 0) {
							udlr++;
						} else {
							diagonal++;
						}
					}
					final int synthesisM = mSum / 5;
					final int synthesisS = sSum / atomCount;
					int synthesisD = 0;
					if (synthesisM == 0) {
						continue;
					}
					if (udlr != 0 && diagonal != 0) {
						synthesisD = 1;
					}
					for (int i = 0; i < 4; i++) {
						temp[x][y].add(new Atom(synthesisM, synthesisS, synthesisD));
						synthesisD += 2;
					}
				} else {
					temp[x][y] = grid[x][y];
				}
			}
		}
		grid = temp;
	}

	private static int convertPos(int r) {
		if (r < 0) {
			r %= N;
			r += N;
			if (r == N) {
				r = 0;
			}
		} else if (r >= N) {
			r %= N;
		}
		return r;
	}

	static class Atom {

		int m;
		int s;
		int d;

		public Atom(int m, int s, int d) {
			super();
			this.m = m;
			this.s = s;
			this.d = d;
		}
	}
}