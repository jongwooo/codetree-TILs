import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static final int[][] dirs = { { -1, 0 }, { 1, 0 }, { 0, -1 }, { 0, 1 } };
	static int n, m, k;
	static int[][] grid;
	static Contract[][] exclusiveContracts;
	static int[] playerDirs;
	static int[][] playerDirPriorities;
	static boolean[] gameOver;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		n = Integer.parseInt(st.nextToken());
		m = Integer.parseInt(st.nextToken());
		k = Integer.parseInt(st.nextToken());
		grid = new int[n][n];
		for (int i = 0; i < n; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < n; j++) {
				grid[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		exclusiveContracts = new Contract[n][n];
		playerDirs = new int[m + 1];
		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < m; i++) {
			playerDirs[i] = Integer.parseInt(st.nextToken()) - 1;
		}
		playerDirPriorities = new int[m * 4][4];
		for (int i = 0; i < m * 4; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < 4; j++) {
				playerDirPriorities[i][j] = Integer.parseInt(st.nextToken()) - 1;
			}
		}
		gameOver = new boolean[m + 1];
		int turnCount = 1;
		for (int i = 0; i < 1_000; i++) {
			playersContract();
			playersMove();
			decreaseTimes();
			if (checkOnlyOnePlayerAlive()) {
				break;
			}
			turnCount++;
		}
		if (turnCount >= 1_000) {
			turnCount = -1;
		}
		System.out.println(turnCount);
	}

	private static void playersContract() {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (grid[i][j] > 0) {
					exclusiveContracts[i][j] = new Contract(k, grid[i][j]);
				}
			}
		}
	}

	private static void playersMove() {
		final List<Integer>[][] temp = new List[n][n];
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				temp[i][j] = new ArrayList<>();
			}
		}
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				if (grid[x][y] == 0) {
					continue;
				}
				final int pid = grid[x][y];
				final int curDir = playerDirs[pid - 1];
				final int[] playerDirPriority = playerDirPriorities[4 * (pid - 1) + curDir];
				boolean moved = false;
				for (final int d : playerDirPriority) {
					final int nx = x + dirs[d][0];
					final int ny = y + dirs[d][1];
					if (0 <= nx && nx < n && 0 <= ny && ny < n && exclusiveContracts[nx][ny] == null) {
						temp[nx][ny].add(pid);
						playerDirs[pid - 1] = d;
						moved = true;
						break;
					}
				}
				if (moved) {
					continue;
				}
				for (final int d : playerDirPriority) {
					final int nx = x + dirs[d][0];
					final int ny = y + dirs[d][1];
					if (0 <= nx && nx < n && 0 <= ny && ny < n && exclusiveContracts[nx][ny].isSamePID(pid)) {
						temp[nx][ny].add(pid);
						playerDirs[pid - 1] = d;
						break;
					}
				}
			}
		}
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (temp[i][j].isEmpty()) {
					grid[i][j] = 0;
					continue;
				}
				if (temp[i][j].size() == 1) {
					grid[i][j] = temp[i][j].get(0);
					continue;
				}
				final int minPlayer = Collections.min(temp[i][j]);
				grid[i][j] = minPlayer;
				for (final int tempId : temp[i][j]) {
					if (tempId != minPlayer) {
						gameOver[tempId] = true;
					}
				}
			}
		}
	}

	private static void decreaseTimes() {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (exclusiveContracts[i][j] == null) {
					continue;
				}
				final Contract contract = exclusiveContracts[i][j];
				contract.decreaseTime();
				if (contract.isTimeZero()) {
					exclusiveContracts[i][j] = null;
				}
			}
		}
	}

	private static boolean checkOnlyOnePlayerAlive() {
		int count = 0;
		for (int i = 1; i <= m; i++) {
			if (!gameOver[i]) {
				count++;
			}
		}
		return count == 1;
	}

	static class Contract {

		int time;
		int pid;

		public Contract(int time, int pid) {
			super();
			this.time = time;
			this.pid = pid;
		}

		public void decreaseTime() {
			time--;
		}

		public boolean isTimeZero() {
			return time == 0;
		}

		public boolean isSamePID(final int pid) {
			return this.pid == pid;
		}
	}
}