import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static final int EMPTY = 0;
	static final int TRAP = 1;
	static final int WALL = 2;
	static final int[][] dirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } };

	static int L, N, Q;
	static int[][] board;
	static int[][] knightBoard;
	static Map<Integer, Knight> knights;
	static boolean[] gameOver;
	static int[] damages;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		L = Integer.parseInt(st.nextToken());
		N = Integer.parseInt(st.nextToken());
		Q = Integer.parseInt(st.nextToken());
		board = new int[L + 2][L + 2];
		initializeBoard();
		for (int i = 1; i <= L; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 1; j <= L; j++) {
				board[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		knightBoard = new int[L + 2][L + 2];
		knights = new HashMap<>();
		for (int pid = 1; pid <= N; pid++) {
			st = new StringTokenizer(br.readLine());
			final int r = Integer.parseInt(st.nextToken());
			final int c = Integer.parseInt(st.nextToken());
			final int h = Integer.parseInt(st.nextToken());
			final int w = Integer.parseInt(st.nextToken());
			final int k = Integer.parseInt(st.nextToken());
			for (int i = 0; i < h; i++) {
				for (int j = 0; j < w; j++) {
					knightBoard[r + i][c + j] = pid;
				}
			}
			knights.put(pid, new Knight(r, c, h, w, k));
		}
		gameOver = new boolean[N + 1];
		damages = new int[N + 1];
		for (int i = 0; i < Q; i++) {
			st = new StringTokenizer(br.readLine());
			final int pid = Integer.parseInt(st.nextToken());
			final int d = Integer.parseInt(st.nextToken());
			if (gameOver[pid] || reachTheWall(pid, d)) {
				continue;
			}
			knightsMove(pid, d);
		}
		int sum = 0;
		for (int i = 1; i <= N; i++) {
			sum += damages[i];
		}
		System.out.println(sum);
	}

	private static void initializeBoard() {
		for (int i = 0; i < L + 2; i++) {
			board[i][0] = WALL;
			board[i][L + 1] = WALL;
			board[0][i] = WALL;
			board[L + 1][i] = WALL;
		}
	}

	private static boolean reachTheWall(final int pid, final int d) {
		final Knight knight = knights.get(pid);
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				if (board[knight.r + i + dirs[d][0]][knight.c + j + dirs[d][1]] == WALL) {
					return true;
				}
			}
		}
		return false;
	}

	private static void knightsMove(final int pid, final int d) {
		final Stack<Integer> stack = new Stack<>();
		stack.add(pid);
		Set<Integer> interactionSet = interaction(pid, d);
		while (!interactionSet.isEmpty()) {
			final Set<Integer> nextInteractionSet = new HashSet<>();
			for (final int nextPid : interactionSet) {
				if (reachTheWall(nextPid, d)) {
					return;
				}
				stack.add(nextPid);
				nextInteractionSet.addAll(interaction(nextPid, d));
			}
			interactionSet = nextInteractionSet;
		}
		while (!stack.isEmpty()) {
			final int p = stack.pop();
			knightMove(p, d);
			if (p != pid) {
				checkTrap(p);
			}
		}
	}

	private static void knightMove(final int pid, final int d) {
		final Knight knight = knights.get(pid);
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				knightBoard[knight.r + i][knight.c + j] = EMPTY;
			}
		}
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				knightBoard[knight.r + i + dirs[d][0]][knight.c + j + dirs[d][1]] = pid;
			}
		}
		knight.r += dirs[d][0];
		knight.c += dirs[d][1];
	}

	private static Set<Integer> interaction(final int pid, final int d) {
		final Knight knight = knights.get(pid);
		final Set<Integer> interactionSet = new HashSet<>();
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				if (knightBoard[knight.r + i + dirs[d][0]][knight.c + j + dirs[d][1]] != pid
						&& knightBoard[knight.r + i + dirs[d][0]][knight.c + j + dirs[d][1]] != EMPTY) {
					interactionSet.add(knightBoard[knight.r + i + dirs[d][0]][knight.c + j + dirs[d][1]]);
				}
			}
		}
		return interactionSet;
	}

	private static void checkTrap(final int pid) {
		final Knight knight = knights.get(pid);
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				if (board[knight.r + i][knight.c + j] == TRAP) {
					damages[pid]++;
					knight.k--;
				}
				if (knight.k == 0) {
					deleteKnightFromBoard(pid);
					return;
				}
			}
		}
	}

	private static void deleteKnightFromBoard(final int pid) {
		final Knight knight = knights.get(pid);
		gameOver[pid] = true;
		damages[pid] = 0;
		knights.remove(pid);
		for (int i = 0; i < knight.h; i++) {
			for (int j = 0; j < knight.w; j++) {
				knightBoard[knight.r + i][knight.c + j] = EMPTY;
			}
		}
	}

	static class Knight {

		int r;
		int c;
		int h;
		int w;
		int k;

		public Knight(int r, int c, int h, int w, int k) {
			super();
			this.r = r;
			this.c = c;
			this.h = h;
			this.w = w;
			this.k = k;
		}
	}
}