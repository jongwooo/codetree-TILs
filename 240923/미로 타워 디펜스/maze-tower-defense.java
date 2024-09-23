import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringBuilder sb;
	static StringTokenizer st;

	static final int[][] attackDirs = { { 0, 1 }, { 1, 0 }, { 0, -1 }, { -1, 0 } }; // → ↓ ← ↑
	static final int[][] mazeDirs = { { 0, -1 }, { 1, 0 }, { 0, 1 }, { -1, 0 } };

	static int n, m;
	static int[][] grid;
	static int[] monsters;
	static Map<Pos, Integer> posIndexMap;
	static int score;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
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
		monsters = new int[n * n];
		Arrays.fill(monsters, -1);
		posIndexMap = new HashMap<>();
		score = 0;
		initialize();
		for (int i = 0; i < m; i++) {
			st = new StringTokenizer(br.readLine());
			final int d = Integer.parseInt(st.nextToken());
			final int p = Integer.parseInt(st.nextToken());
			attack(d, p);
			tideUp();
			while (true) {
				if (!removeRepeatedMonsters()) {
					break;
				}
				tideUp();
			}
			pairMonsterNums();
		}
		System.out.println(score);
	}

	private static void initialize() {
		int x = n / 2;
		int y = n / 2;
		int index = 0;
		int dist = 1;
		int dir = 0;
		int move = 0;
		while (true) {
			for (int i = 0; i < dist; i++) {
				monsters[index] = grid[x][y];
				posIndexMap.put(new Pos(x, y), index);
				final int nx = x + mazeDirs[dir][0];
				final int ny = y + mazeDirs[dir][1];
				if (nx == 0 && ny == -1) {
					return;
				}
				index++;
				x = nx;
				y = ny;
			}
			move++;
			dir = (dir + 1) % 4;
			if (move == 2) {
				dist++;
				move = 0;
			}
		}
	}

	private static void attack(final int d, final int p) {
		final int x = n / 2;
		final int y = n / 2;
		for (int i = 1; i <= p; i++) {
			final int nx = x + attackDirs[d][0] * i;
			final int ny = y + attackDirs[d][1] * i;
			final int index = posIndexMap.get(new Pos(nx, ny));
			score += monsters[index];
			monsters[index] = -1;
		}
	}

	private static void tideUp() {
		final int[] temp = new int[n * n];
		int index = 0;
		for (int i = 0; i < n * n; i++) {
			if (monsters[i] == -1) {
				continue;
			}
			temp[index++] = monsters[i];
		}
		monsters = temp;
	}

	private static boolean removeRepeatedMonsters() {
		boolean flag = false;
		int target = 0;
		int count = 0;
		for (int i = 0; i < n * n; i++) {
			if (monsters[i] == monsters[target]) {
				count++;
			} else {
				if (count >= 4) {
					flag = true;
					score += monsters[target] * count;
					for (int j = target; j < i; j++) {
						monsters[j] = -1;
					}
				}
				target = i;
				count = 1;
			}
		}
		return flag;
	}

	private static void pairMonsterNums() {
		final int[] newMonsters = new int[n * n];
		final Queue<Integer> group = new ArrayDeque<>();
		int index = 1;
		for (int i = 1; i < n * n; i++) {
			if (group.isEmpty()) {
				group.add(monsters[i]);
			} else if (monsters[i] == group.peek()) {
				group.add(monsters[i]);
			} else {
				if (index == n * n) {
					break;
				}
				newMonsters[index++] = group.size();
				newMonsters[index++] = group.peek();
				group.clear();
				group.add(monsters[i]);
			}
		}
		monsters = newMonsters;
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