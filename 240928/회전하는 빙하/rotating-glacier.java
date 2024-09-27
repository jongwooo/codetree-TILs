import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringBuilder sb;
	static StringTokenizer st;

	static final int[][] dirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } };

	static int n, q;
	static int gridSize;
	static int[][] grid;
	static int iceSum;
	static int maxClusterSize;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
		st = new StringTokenizer(br.readLine());
		n = Integer.parseInt(st.nextToken());
		q = Integer.parseInt(st.nextToken());
		gridSize = (int) Math.pow(2, n);
		grid = new int[gridSize][gridSize];
		for (int i = 0; i < gridSize; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < gridSize; j++) {
				grid[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < q; i++) {
			final int level = Integer.parseInt(st.nextToken());
			if (level > 0) {
				rotate(level);
			}
			melt();
		}
		iceSum = 0;
		maxClusterSize = 0;
		bfs();
		sb.append(iceSum)
				.append("\n")
				.append(maxClusterSize);
		System.out.println(sb);
	}

	private static void rotate(final int level) {
		final int[][] temp = new int[gridSize][gridSize];
		final int size = (int) Math.pow(2, level);
		final int halfSize = (int) Math.pow(2, level - 1);
		for (int x = 0; x < gridSize; x += size) {
			for (int y = 0; y < gridSize; y += size) {
				if (halfSize == 1) {
					for (int i = 0; i <= halfSize; i++) {
						for (int j = 0; j <= halfSize; j++) {
							temp[x + j][halfSize + y - i] = grid[x + i][y + j];
						}
					}
				} else {
					for (int i = 0; i < size; i += halfSize) {
						for (int j = 0; j < size; j += halfSize) {
							for (int k = 0; k < halfSize; k++) {
								for (int m = 0; m < halfSize; m++) {
									temp[x + j + k][halfSize + y - i + m] = grid[x + i + k][y + j + m];
								}
							}
						}
					}
				}
			}
		}
		grid = temp;
	}

	private static void melt() {
		final Queue<Pos> meltCandidates = new ArrayDeque<>();
		for (int x = 0; x < gridSize; x++) {
			for (int y = 0; y < gridSize; y++) {
				int count = 0;
				for (int d = 0; d < 4; d++) {
					final int nx = x + dirs[d][0];
					final int ny = y + dirs[d][1];
					if (0 <= nx && nx < gridSize && 0 <= ny && ny < gridSize && grid[nx][ny] > 0) {
						count++;
					}
				}
				if (count < 3 && grid[x][y] > 0) {
					meltCandidates.add(new Pos(x, y));
				}
			}
		}
		for (final Pos pos : meltCandidates) {
			grid[pos.x][pos.y]--;
		}
	}

	private static void bfs() {
		final boolean[][] visited = new boolean[gridSize][gridSize];
		for (int i = 0; i < gridSize; i++) {
			for (int j = 0; j < gridSize; j++) {
				int clusterSize = 0;
				if (visited[i][j] || grid[i][j] == 0) {
					continue;
				}
				final Queue<Pos> queue = new ArrayDeque<>();
				queue.add(new Pos(i, j));
				visited[i][j] = true;
				while (!queue.isEmpty()) {
					final Pos pos = queue.poll();
					iceSum += grid[pos.x][pos.y];
					clusterSize++;
					for (int d = 0; d < 4; d++) {
						final int nx = pos.x + dirs[d][0];
						final int ny = pos.y + dirs[d][1];
						if (0 <= nx && nx < gridSize && 0 <= ny && ny < gridSize && !visited[nx][ny]
								&& grid[nx][ny] > 0) {
							queue.add(new Pos(nx, ny));
							visited[nx][ny] = true;
						}
					}
				}
				if (maxClusterSize < clusterSize) {
					maxClusterSize = clusterSize;
				}
			}
		}
	}

	static class Pos {

		final int x;
		final int y;

		public Pos(final int x, final int y) {
			this.x = x;
			this.y = y;
		}
	}
}