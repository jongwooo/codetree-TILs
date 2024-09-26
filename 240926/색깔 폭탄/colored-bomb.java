import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static final int EMPTY = -2;
	static final int STONE = -1;
	static final int RED_BOOM = 0;
	static final int[][] dirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } };

	static int n, m;
	static int[][] grid;
	static int score;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		n = Integer.parseInt(st.nextToken());
		m = Integer.parseInt(st.nextToken());
		grid = new int[n][n];
		for (int i = 0; i < n; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < n; j++) {
				grid[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		score = 0;
		while (true) {
			if (!findAndEliminateMaxSizeBoomBundle()) {
				break;
			}
			gravity();
			rotate();
			gravity();
		}
		System.out.println(score);
	}

	private static boolean findAndEliminateMaxSizeBoomBundle() {
		final List<BoomBundle> candidates = new ArrayList<>();
		final boolean[][] visited = new boolean[n][n];
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				if (!visited[x][y] && grid[x][y] >= 0) {
					final BoomBundle boomBundle = bfs(x, y, visited);
					if (boomBundle.bundle.size() > 1) {
						final Pos pos = findReferencePoint(boomBundle.bundle);
						if (pos.x == -1 && pos.y == -1) {
							continue;
						}
						candidates.add(new BoomBundle(boomBundle.bundle, boomBundle.redCount, pos.x, pos.y));
					}
				}
			}
		}
		if (candidates.isEmpty()) {
			return false;
		}
		Collections.sort(candidates);
		final BoomBundle boomBundle = candidates.get(0);
		for (final Pos pos : boomBundle.bundle) {
			grid[pos.x][pos.y] = EMPTY;
		}
		final int c = boomBundle.bundle.size();
		score += c * c;
		return true;
	}

	private static Pos findReferencePoint(final List<Pos> bundle) {
		Collections.sort(bundle);
		int rx = -1;
		int ry = -1;
		for (final Pos pos : bundle) {
			if (grid[pos.x][pos.y] != RED_BOOM) {
				rx = pos.x;
				ry = pos.y;
				break;
			}
		}
		return new Pos(rx, ry);
	}

	private static BoomBundle bfs(final int sx, final int sy, final boolean[][] visited) {
		final Queue<Pos> queue = new ArrayDeque<>();
		queue.add(new Pos(sx, sy));
		final List<Pos> bundle = new ArrayList<>();
		final boolean[][] temp = new boolean[n][n];
		temp[sx][sy] = true;
		final int color = grid[sx][sy];
		int redCount = 0;
		while (!queue.isEmpty()) {
			final Pos pos = queue.poll();
			bundle.add(pos);
			if (grid[pos.x][pos.y] == RED_BOOM) {
				redCount++;
			}
			for (int d = 0; d < 4; d++) {
				final int nx = pos.x + dirs[d][0];
				final int ny = pos.y + dirs[d][1];
				if (0 <= nx && nx < n && 0 <= ny && ny < n && grid[nx][ny] != EMPTY && grid[nx][ny] != STONE
						&& !temp[nx][ny] && (grid[nx][ny] == RED_BOOM || grid[nx][ny] == color)) {
					queue.add(new Pos(nx, ny));
					temp[nx][ny] = true;
				}
			}
		}
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (grid[i][j] != RED_BOOM && temp[i][j]) {
					visited[i][j] = temp[i][j];
				}
			}
		}
		return new BoomBundle(bundle, redCount);
	}

	private static void rotate() {
		final int[][] temp = new int[n][n];
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				temp[x][y] = grid[y][n - x - 1];
			}
		}
		grid = temp;
	}

	private static void gravity() {
		for (int y = 0; y < n; y++) {
			for (int x = n - 1; x >= 0; x--) {
				int curX = x;
				while (curX + 1 < n && grid[curX][y] != STONE && grid[curX + 1][y] == EMPTY) {
					final int temp = grid[curX + 1][y];
					grid[curX + 1][y] = grid[curX][y];
					grid[curX][y] = temp;
					curX++;
				}
			}
		}
	}

	static class Pos implements Comparable<Pos> {

		final int x;
		final int y;

		public Pos(final int x, final int y) {
			this.x = x;
			this.y = y;
		}

		@Override
		public int compareTo(final Pos other) {
			if (this.x != other.x) {
				return other.x - this.x;
			}
			return this.y - other.y;
		}
	}

	static class BoomBundle implements Comparable<BoomBundle> {

		final List<Pos> bundle;
		final int redCount;
		final int rx;
		final int ry;

		public BoomBundle(final List<Pos> bundle, final int redCount) {
			this.bundle = bundle;
			this.redCount = redCount;
			rx = -1;
			ry = -1;
		}

		public BoomBundle(final List<Pos> bundle, final int redCount, final int rx, final int ry) {
			super();
			this.bundle = bundle;
			this.redCount = redCount;
			this.rx = rx;
			this.ry = ry;
		}

		@Override
		public int compareTo(final BoomBundle other) {
			if (this.bundle.size() != other.bundle.size()) {
				return other.bundle.size() - this.bundle.size();
			}
			if (this.redCount != other.redCount) {
				return this.redCount - other.redCount;
			}
			if (this.rx != other.rx) {
				return other.rx - this.rx;
			}
			return this.ry - other.ry;
		}
	}
}