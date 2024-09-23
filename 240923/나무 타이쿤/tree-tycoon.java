import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {
	
	static BufferedReader br;
	static StringTokenizer st;
	
	static final int[][] moveDirs = {{0, 1}, {-1, 1}, {-1, 0}, {-1, -1}, {0, -1}, {1, -1}, {1, 0}, {1, 1}};
	static final int[][] treeDirs = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
	
	static int n, m;
	static int[][] treeHeights;
	static List<Pos> supplements;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		n = Integer.parseInt(st.nextToken());
		m = Integer.parseInt(st.nextToken());
		treeHeights = new int[n][n];
		for (int i = 0; i < n; i++) {
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < n; j++) {
				treeHeights[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		supplements = new ArrayList<>();
		addInitialSupplements();
		for (int i = 0; i < m; i++) {
			st = new StringTokenizer(br.readLine());
			final int d = Integer.parseInt(st.nextToken()) - 1;
			final int p = Integer.parseInt(st.nextToken());
			moveSuppplements(d, p);
			injectSupplementsAndGrowth();
			cutTreesAndAddSupplements();
		}
		System.out.println(sumRemainigTreeHeights());
	}
	
	private static void addInitialSupplements() {
		supplements.add(new Pos(n - 1, 0));
		supplements.add(new Pos(n - 1, 1));
		supplements.add(new Pos(n - 2, 0));
		supplements.add(new Pos(n - 2, 1));
	}
	
	private static void moveSuppplements(final int d, final int p) {
		final List<Pos> temp = new ArrayList<>();
		for (final Pos supplement : supplements) {
			final int nx = (n + supplement.x + moveDirs[d][0] * p) % n;
			final int ny = (n + supplement.y + moveDirs[d][1] * p) % n;
			temp.add(new Pos(nx, ny));
		}
		supplements = temp;
	}

	private static void injectSupplementsAndGrowth() {
		for (final Pos supplenment : supplements) {
			treeHeights[supplenment.x][supplenment.y]++;
		}
		for (final Pos supplenment : supplements) {
			for (int d = 0; d < 4; d++) {
				final int nx = supplenment.x + treeDirs[d][0];
				final int ny = supplenment.y + treeDirs[d][1];
				if (0 <= nx && nx < n && 0 <= ny && ny < n && 1 <= treeHeights[nx][ny]) {
					treeHeights[supplenment.x][supplenment.y]++;
				}
			}
		}
	}

	private static void cutTreesAndAddSupplements() {
		final List<Pos> temp = new ArrayList<>();
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				if (!supplements.contains(new Pos(x, y)) && 2 <= treeHeights[x][y]) {
					treeHeights[x][y] -= 2;
					temp.add(new Pos(x, y));
				}
			}
		}
		supplements = temp;
	}
	
	private static int sumRemainigTreeHeights() {
		int heights = 0;
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				heights += treeHeights[x][y];
			}
		}
		return heights;
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
	}
}