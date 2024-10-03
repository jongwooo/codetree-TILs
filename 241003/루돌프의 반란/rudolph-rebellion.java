import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringBuilder sb;
	static StringTokenizer st;

	static final int EMPTY = 0;
	static final int RUDOLPH = -1;
	static final int[][] santaDirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } }; // 상 우 하 좌

	static int N, M, P, C, D;
	static int[][] board;
	static int rr, rc;
	static Map<Integer, int[]> santa;
	static int santaCount;
	static int[] panicTime;
	static boolean[] gameOver;
	static int[] score;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
		st = new StringTokenizer(br.readLine());
		N = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		P = Integer.parseInt(st.nextToken());
		C = Integer.parseInt(st.nextToken());
		D = Integer.parseInt(st.nextToken());
		board = new int[N + 1][N + 1];
		st = new StringTokenizer(br.readLine());
		rr = Integer.parseInt(st.nextToken());
		rc = Integer.parseInt(st.nextToken());
		board[rr][rc] = RUDOLPH;
		santa = new HashMap<>();
		santaCount = P;
		panicTime = new int[P + 1];
		gameOver = new boolean[P + 1];
		score = new int[P + 1];
		for (int i = 0; i < P; i++) {
			st = new StringTokenizer(br.readLine());
			final int pn = Integer.parseInt(st.nextToken());
			final int sr = Integer.parseInt(st.nextToken());
			final int sc = Integer.parseInt(st.nextToken());
			board[sr][sc] = pn;
			santa.put(pn, new int[] { sr, sc });
		}
		for (int t = 1; t <= M; t++) {
			turn(t);
			if (santaCount == 0) {
				break;
			}
		}
		for (int i = 1; i <= P; i++) {
			sb.append(score[i])
					.append(" ");
		}
		System.out.println(sb);
	}

	private static boolean inBoard(final int x, final int y) {
		return 0 < x && x <= N && 0 < y && y <= N;
	}

	private static int distance(final int r1, final int c1, final int r2, final int c2) {
		return (r1 - r2) * (r1 - r2) + (c1 - c2) * (c1 - c2);
	}

	private static void turn(final int time) {
		rudolphMove(time);
		if (santaCount == 0) {
			return;
		}
		for (int pn = 1; pn <= P; pn++) {
			if (gameOver[pn]) {
				continue;
			}
			if (panicTime[pn] < time) {
				santaMove(time, pn);
			}
			if (santaCount == 0) {
				return;
			}
		}
		for (int pn = 1; pn <= P; pn++) {
			if (!gameOver[pn]) {
				score[pn]++;
			}
		}
	}

	private static void rudolphMove(final int time) {
		final List<int[]> candidates = new ArrayList<>();
		for (int pn = 1; pn <= P; pn++) {
			if (gameOver[pn]) {
				continue;
			}
			final int[] santaPos = santa.get(pn);
			final int dist = distance(rr, rc, santaPos[0], santaPos[1]);
			candidates.add(new int[] { dist, santaPos[0], santaPos[1] });
		}
		Collections.sort(candidates, (o1, o2) -> {
			if (o1[0] != o2[0]) {
				return Integer.compare(o1[0], o2[0]);
			}
			if (o1[1] != o2[1]) {
				return Integer.compare(o2[1], o1[1]);
			}
			return Integer.compare(o2[2], o1[2]);
		});
		final int[] target = candidates.get(0);
		board[rr][rc] = EMPTY;
		int dr = 0;
		int dc = 0;
		if (target[1] > rr) {
			dr = 1;
		} else if (target[1] < rr) {
			dr = -1;
		}
		if (target[2] > rc) {
			dc = 1;
		} else if (target[2] < rc) {
			dc = -1;
		}
		final int nr = rr + dr;
		final int nc = rc + dc;
		if (board[nr][nc] != EMPTY) {
			crushRudolphToSanta(time, nr, nc, dr, dc);
		}
		board[nr][nc] = RUDOLPH;
		rr = nr;
		rc = nc;
	}

	private static void crushRudolphToSanta(final int time, final int sr, final int sc, final int dr, final int dc) {
		final int pn = board[sr][sc];
		board[sr][sc] = EMPTY;
		panicTime[pn] = time + 1;
		score[pn] += C;
		final int nsr = sr + dr * C;
		final int nsc = sc + dc * C;
		if (!inBoard(nsr, nsc)) {
			santa.remove(pn);
			gameOver[pn] = true;
			santaCount--;
			return;
		}
		if (board[nsr][nsc] != EMPTY) {
			interaction(nsr, nsc, dr, dc);
		}
		board[nsr][nsc] = pn;
		santa.put(pn, new int[] { nsr, nsc });
	}

	private static void santaMove(final int time, final int pn) {
		final int[] santaPos = santa.get(pn);
		final int sr = santaPos[0];
		final int sc = santaPos[1];
		final int curDist = distance(rr, rc, sr, sc);
		final List<int[]> candidates = new ArrayList<>();
		for (int d = 0; d < 4; d++) {
			final int nsr = sr + santaDirs[d][0];
			final int nsc = sc + santaDirs[d][1];
			final int dist = distance(rr, rc, nsr, nsc);
			if (inBoard(nsr, nsc) && (board[nsr][nsc] == EMPTY || board[nsr][nsc] == RUDOLPH) && dist < curDist) {
				candidates.add(new int[] { dist, d, nsr, nsc });
			}
		}
		if (candidates.isEmpty()) {
			return;
		}
		Collections.sort(candidates, (o1, o2) -> {
			if (o1[0] != o2[0]) {
				return Integer.compare(o1[0], o2[0]);
			}
			return Integer.compare(o1[1], o2[1]);
		});
		final int[] target = candidates.get(0);
		final int d = target[1];
		final int nsr = target[2];
		final int nsc = target[3];
		board[sr][sc] = EMPTY;
		if (board[nsr][nsc] == RUDOLPH) {
			crushSantaToRudolph(time, pn, d);
		} else {
			board[nsr][nsc] = pn;
			santa.put(pn, new int[] { nsr, nsc });
		}
	}

	private static void crushSantaToRudolph(final int time, final int pn, final int d) {
		panicTime[pn] = time + 1;
		score[pn] += D;
		final int nsr = rr - santaDirs[d][0] * D;
		final int nsc = rc - santaDirs[d][1] * D;
		if (!inBoard(nsr, nsc)) {
			santa.remove(pn);
			gameOver[pn] = true;
			santaCount--;
			return;
		}
		if (board[nsr][nsc] != EMPTY) {
			interaction(nsr, nsc, -santaDirs[d][0], -santaDirs[d][1]);
		}
		board[nsr][nsc] = pn;
		santa.put(pn, new int[] { nsr, nsc });
	}

	private static void interaction(final int r, final int c, final int dr, final int dc) {
		final int pn = board[r][c];
		board[r][c] = EMPTY;
		final int nsr = r + dr;
		final int nsc = c + dc;
		if (!inBoard(nsr, nsc)) {
			santa.remove(pn);
			gameOver[pn] = true;
			santaCount--;
			return;
		}
		if (board[nsr][nsc] != EMPTY) {
			interaction(nsr, nsc, dr, dc);
		}
		board[nsr][nsc] = pn;
		santa.put(pn, new int[] { nsr, nsc });
	}
}