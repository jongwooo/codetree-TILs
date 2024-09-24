import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Queue;
import java.util.Set;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringBuilder sb;
	static StringTokenizer st;

	static final int[][] exitDirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } };

	static int R, C, K;
	static int[][] grid;
	static Set<Pos> exitSet;
	static int rowSum;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
		st = new StringTokenizer(br.readLine());
		R = Integer.parseInt(st.nextToken());
		C = Integer.parseInt(st.nextToken());
		K = Integer.parseInt(st.nextToken());
		exitSet = new HashSet<>();
		initializeGrid();
		rowSum = 0;
		int num = 2;
		for (int k = 0; k < K; k++) {
			st = new StringTokenizer(br.readLine());
			int cy = Integer.parseInt(st.nextToken());
			int d = Integer.parseInt(st.nextToken());
			int cx = 1;
			while (true) {
				if (grid[cx + 1][cy - 1] + grid[cx + 2][cy] + grid[cx + 1][cy + 1] == 0) {
					cx++;
				} else if (grid[cx - 1][cy - 1] + grid[cx][cy - 2] + grid[cx + 1][cy - 1] + grid[cx + 1][cy - 2]
						+ grid[cx + 2][cy - 1] == 0) {
					cx++;
					cy--;
					d = (d - 1) % 4;
				} else if (grid[cx + 1][cy + 1] + grid[cx][cy + 2] + grid[cx - 1][cy + 1] + grid[cx + 1][cy + 2]
						+ grid[cx + 2][cy + 1] == 0) {
					cx++;
					cy++;
					d = (d + 1) % 4;
				} else {
					break;
				}
			}
			if (cx < 4) {
				initializeGrid();
				exitSet.clear();
				continue;
			}
			grid[cx + 1][cy] = num;
			grid[cx - 1][cy] = num;
			for (int i = -1; i <= 1; i++) {
				grid[cx][cy + i] = num;
			}
			num++;
			d = (d + 4) % 4;
			exitSet.add(new Pos(cx + exitDirs[d][0], cy + exitDirs[d][1]));
			rowSum += bfs(cx, cy);
		}
		System.out.println(rowSum);
	}

	private static void initializeGrid() {
		grid = new int[R + 4][C + 2];
		for (int i = 0; i < R + 4; i++) {
			grid[i][0] = 1;
			grid[i][C + 1] = 1;
		}
		for (int i = 1; i < C + 1; i++) {
			grid[R + 3][i] = 1;
		}
	}

	private static int bfs(final int sx, final int sy) {
		final Queue<Pos> queue = new ArrayDeque<>();
		queue.add(new Pos(sx, sy));
		final boolean[][] visited = new boolean[R + 4][C + 2];
		visited[sx][sy] = true;
		int maxRow = 0;
		while (!queue.isEmpty()) {
			final Pos pos = queue.poll();
			if (maxRow < pos.x) {
				maxRow = pos.x;
			}
			for (int d = 0; d < 4; d++) {
				final int nx = pos.x + exitDirs[d][0];
				final int ny = pos.y + exitDirs[d][1];
				if (!visited[nx][ny] && (grid[pos.x][pos.y] == grid[nx][ny]
						|| (exitSet.contains(new Pos(pos.x, pos.y)) && grid[nx][ny] > 1))) {
					queue.add(new Pos(nx, ny));
					visited[nx][ny] = true;
				}
			}
		}
		return maxRow - 2;
	}

	static class Pos {

		final int x;
		final int y;

		public Pos(final int x, final int y) {
			this.x = x;
			this.y = y;
		}

		@Override
		public boolean equals(Object object) {
			final Pos other = (Pos) object;
			return this.x == other.x && this.y == other.y;
		}

		@Override
		public int hashCode() {
			return 100 * x + y;
		}
	}
}