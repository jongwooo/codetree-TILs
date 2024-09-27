import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static final double[][] p0 = { { 0, 0, 0.02, 0, 0 }, { 0, 0.1, 0.07, 0.01, 0 }, { 0.05, 0, 0, 0, 0 },
			{ 0, 0.1, 0.07, 0.01, 0 }, { 0, 0, 0.02, 0, 0 } };
	static final double[][] p1 = { { 0, 0, 0, 0, 0 }, { 0, 0.01, 0, 0.01, 0 }, { 0.02, 0.07, 0, 0.07, 0.02 },
			{ 0, 0.1, 0, 0.1, 0 }, { 0, 0, 0.05, 0, 0 } };
	static final double[][] p2 = { { 0, 0, 0.02, 0, 0 }, { 0, 0.01, 0.07, 0.1, 0 }, { 0, 0, 0, 0, 0.05 },
			{ 0, 0.01, 0.07, 0.1, 0 }, { 0, 0, 0.02, 0, 0 } };
	static final double[][] p3 = { { 0, 0, 0.05, 0, 0 }, { 0, 0.1, 0, 0.1, 0 }, { 0.02, 0.07, 0, 0.07, 0.02 },
			{ 0, 0.01, 0, 0.01, 0 }, { 0, 0, 0, 0, 0 } };
	static final double[][][] proportions = { p0, p1, p2, p3 };
	static final int[][] alphas = { { 2, 1 }, { 3, 2 }, { 2, 3 }, { 1, 2 } };
	static final int[][] moveDirs = { { 0, -1 }, { 1, 0 }, { 0, 1 }, { -1, 0 } }; // 왼쪽 - 아래쪽 - 오른쪽 - 위쪽

	static int n;
	static int[][] grid;
	static int dustOut;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		n = Integer.parseInt(br.readLine());
		grid = new int[n][n];
		for (int i = 0; i < n; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < n; j++) {
				grid[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		dustOut = 0;
		wipeFloor();
		System.out.println(dustOut);
	}

	private static void wipeFloor() {
		int move = 0;
		int dist = 1;
		int d = 0;
		int x = n / 2;
		int y = n / 2;
		while (true) {
			for (int i = 0; i < dist; i++) {
				final int nx = x + moveDirs[d][0];
				final int ny = y + moveDirs[d][1];
				if (nx == 0 && ny == -1) {
					return;
				}
				cleanDust(d, nx, ny);
				x = nx;
				y = ny;
			}
			d = (d + 1) % 4;
			move++;
			if (move == 2) {
				move = 0;
				dist++;
			}
		}
	}

	private static void cleanDust(final int d, final int x, final int y) {
		int dust = grid[x][y];
		grid[x][y] = 0;
		int left = dust;
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 5; j++) {
				final int scatteredDust = (int) (proportions[d][i][j] * dust);
				left -= scatteredDust;
				final int nx = x + i - 2;
				final int ny = y + j - 2;
				if (0 <= nx && nx < n && 0 <= ny && ny < n) {
					grid[nx][ny] += scatteredDust;
				} else {
					dustOut += scatteredDust;
				}
			}
		}
		final int ax = x + alphas[d][0] - 2;
		final int ay = y + alphas[d][1] - 2;
		if (0 <= ax && ax < n && 0 <= ay && ay < n) {
			grid[ax][ay] += left;
		} else {
			dustOut += left;
		}
	}
}