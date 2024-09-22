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
	static StringBuilder sb;
	static StringTokenizer st;

	static int[] dirX = { -1, 0, 0, 1 };
	static int[] dirY = { 0, 1, -1, 0 };
	static int K, M;
	static int[][] grid;
	static Queue<Integer> nextItems;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
		st = new StringTokenizer(br.readLine());
		K = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		grid = new int[5][5];
		for (int i = 0; i < 5; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < 5; j++) {
				grid[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		nextItems = new ArrayDeque<>();
		st = new StringTokenizer(br.readLine());
		while (st.hasMoreTokens()) {
			nextItems.add(Integer.parseInt(st.nextToken()));
		}
		for (int k = 0; k < K; k++) {
			final Coordinate coordinate = findMaxValueCoordinate();
			if (coordinate.value == 0) {
				break;
			}
			updateGrid(coordinate.d, coordinate.sx, coordinate.sy);
			int removedItemCount = removeUsedItems();
			int itemValueSum = 0;
			while (removedItemCount > 0) {
				itemValueSum += removedItemCount;
				fillNextItemsToEmptySpace();
				removedItemCount = removeUsedItems();
			}
			sb.append(itemValueSum)
					.append(" ");
		}
		System.out.println(sb);
	}

	private static void rotate90(final int sx, final int sy) {
		final int[][] temp = new int[5][5];
		for (int x = sx; x < sx + 3; x++) {
			for (int y = sy; y < sy + 3; y++) {
				final int ox = x - sx;
				final int oy = y - sy;
				final int rx = oy;
				final int ry = 3 - ox - 1;
				temp[sx + rx][sy + ry] = grid[x][y];
			}
		}
		for (int x = sx; x < sx + 3; x++) {
			for (int y = sy; y < sy + 3; y++) {
				grid[x][y] = temp[x][y];
			}
		}
	}

	private static Coordinate findMaxValueCoordinate() {
		final List<Coordinate> coordinates = new ArrayList<>();
		for (int sx = 0; sx < 3; sx++) {
			for (int sy = 0; sy < 3; sy++) {
				for (int d = 0; d < 4; d++) {
					rotate90(sx, sy);
					if (d == 3) {
						break;
					}
					final boolean[][] visited = new boolean[5][5];
					int value = 0;
					for (int x = 0; x < 5; x++) {
						for (int y = 0; y < 5; y++) {
							if (!visited[x][y]) {
								value += bfs1(x, y, visited);
							}
						}
					}
					coordinates.add(new Coordinate(value, d, sx, sy));
				}
			}
		}
		Collections.sort(coordinates);
		return coordinates.get(0);
	}

	private static int bfs1(final int sx, final int sy, final boolean[][] visited) {
		final Queue<Pos> queue = new ArrayDeque<>();
		queue.add(new Pos(sx, sy));
		visited[sx][sy] = true;
		final int number = grid[sx][sy];
		int count = 1;
		while (!queue.isEmpty()) {
			final Pos pos = queue.poll();
			for (int d = 0; d < 4; d++) {
				final int nx = pos.x + dirX[d];
				final int ny = pos.y + dirY[d];
				if (0 <= nx && nx < 5 && 0 <= ny && ny < 5 && !visited[nx][ny] && grid[nx][ny] == number) {
					queue.add(new Pos(nx, ny));
					visited[nx][ny] = true;
					count++;
				}
			}
		}
		if (count < 3) {
			return 0;
		}
		return count;
	}

	private static void updateGrid(final int dir, final int sx, final int sy) {
		for (int d = 0; d < dir + 1; d++) {
			rotate90(sx, sy);
		}
	}

	private static int removeUsedItems() {
		int count = 0;
		final boolean[][] visited = new boolean[5][5];
		for (int x = 0; x < 5; x++) {
			for (int y = 0; y < 5; y++) {
				count += bfs2(x, y, visited);
			}
		}
		return count;
	}

	private static int bfs2(final int sx, final int sy, final boolean[][] visited) {
		final Queue<Pos> sameNumberPos = new ArrayDeque<>();
		sameNumberPos.add(new Pos(sx, sy));
		final Queue<Pos> queue = new ArrayDeque<>();
		queue.add(new Pos(sx, sy));
		visited[sx][sy] = true;
		final int number = grid[sx][sy];
		while (!queue.isEmpty()) {
			final Pos pos = queue.poll();
			for (int d = 0; d < 4; d++) {
				final int nx = pos.x + dirX[d];
				final int ny = pos.y + dirY[d];
				if (0 <= nx && nx < 5 && 0 <= ny && ny < 5 && !visited[nx][ny] && grid[nx][ny] == number) {
					final Pos nextPos = new Pos(nx, ny);
					queue.add(nextPos);
					sameNumberPos.add(nextPos);
					visited[nx][ny] = true;
				}
			}
		}
		if (sameNumberPos.size() < 3) {
			return 0;
		}
		int count = 0;
		while (!sameNumberPos.isEmpty()) {
			final Pos pos = sameNumberPos.poll();
			grid[pos.x][pos.y] = 0;
			count++;
		}
		return count;
	}

	private static void fillNextItemsToEmptySpace() {
		for (int y = 0; y < 5; y++) {
			for (int x = 4; x >= 0; x--) {
				if (grid[x][y] == 0) {
					grid[x][y] = nextItems.poll();
				}
			}
		}
	}

	private static class Pos {

		final int x;
		final int y;

		public Pos(final int x, final int y) {
			this.x = x;
			this.y = y;
		}
	}

	private static class Coordinate implements Comparable<Coordinate> {

		final int value;
		final int d;
		final int sx;
		final int sy;

		public Coordinate(final int value, final int d, final int sx, final int sy) {
			super();
			this.value = value;
			this.d = d;
			this.sx = sx;
			this.sy = sy;
		}

		@Override
		public int compareTo(final Coordinate other) {
			// TODO Auto-generated method stub
			if (this.value != other.value) {
				return other.value - this.value;
			}
			if (this.d != other.d) {
				return this.d - other.d;
			}
			if (this.sy != other.sy) {
				return this.sy - other.sy;
			}
			return this.sx - other.sx;
		}
	}
}