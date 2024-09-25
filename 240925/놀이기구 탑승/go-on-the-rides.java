import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringBuilder sb;
	static StringTokenizer st;

	static final int[][] dirs = { { -1, 0 }, { 0, 1 }, { 1, 0 }, { 0, -1 } };
	static final int[] scores = { 0, 1, 10, 100, 1_000 };

	static int n;
	static int[][] grid;
	static int[][] favoriteFriendInfos;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		sb = new StringBuilder();
		n = Integer.parseInt(br.readLine());
		grid = new int[n][n];
		favoriteFriendInfos = new int[n * n + 1][4];
		for (int i = 0; i < n * n; i++) {
			st = new StringTokenizer(br.readLine());
			final int n0 = Integer.parseInt(st.nextToken());
			for (int j = 0; j < 4; j++) {
				favoriteFriendInfos[n0][j] = Integer.parseInt(st.nextToken());
			}
			findSeat(n0);
		}
		int score = 0;
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				score += scores[countFavoriteFriends(grid[x][y], x, y)];
			}
		}
		System.out.println(score);
	}

	private static void findSeat(final int student) {
		final List<SeatInfo> candidates = new ArrayList<>();
		for (int x = 0; x < n; x++) {
			for (int y = 0; y < n; y++) {
				if (grid[x][y] == 0) {
					final int favoriteFriendsCount = countFavoriteFriends(student, x, y);
					final int emptySeatsCount = countEmptySeats(x, y);
					candidates.add(new SeatInfo(favoriteFriendsCount, emptySeatsCount, x, y));
				}
			}
		}
		Collections.sort(candidates);
		final SeatInfo target = candidates.get(0);
		grid[target.x][target.y] = student;
	}

	private static int countFavoriteFriends(final int student, final int x, final int y) {
		int count = 0;
		for (int d = 0; d < 4; d++) {
			final int nx = x + dirs[d][0];
			final int ny = y + dirs[d][1];
			if (inRange(nx, ny) && grid[nx][ny] > 0) {
				if (isFavoriteFriend(student, grid[nx][ny])) {
					count++;
				}
			}
		}
		return count;
	}

	private static boolean isFavoriteFriend(final int n0, final int target) {
		for (final int student : favoriteFriendInfos[n0]) {
			if (student == target) {
				return true;
			}
		}
		return false;
	}

	private static int countEmptySeats(final int x, final int y) {
		int count = 0;
		for (int d = 0; d < 4; d++) {
			final int nx = x + dirs[d][0];
			final int ny = y + dirs[d][1];
			if (inRange(nx, ny) && grid[nx][ny] == 0) {
				count++;
			}
		}
		return count;
	}

	private static boolean inRange(final int x, final int y) {
		return 0 <= x && x < n && 0 <= y && y < n;
	}

	static class SeatInfo implements Comparable<SeatInfo> {

		final int favoriteFriendsCount;
		final int emptySeatsCount;
		final int x;
		final int y;

		public SeatInfo(int favoriteFriendsCount, int emptySeatsCount, int x, int y) {
			super();
			this.favoriteFriendsCount = favoriteFriendsCount;
			this.emptySeatsCount = emptySeatsCount;
			this.x = x;
			this.y = y;
		}

		@Override
		public int compareTo(final SeatInfo other) {
			if (this.favoriteFriendsCount != other.favoriteFriendsCount) {
				return other.favoriteFriendsCount - this.favoriteFriendsCount;
			}
			if (this.emptySeatsCount != other.emptySeatsCount) {
				return other.emptySeatsCount - this.emptySeatsCount;
			}
			if (this.y != other.y) {
				return this.y - other.y;
			}
			return this.x - other.x;
		}
	}
}