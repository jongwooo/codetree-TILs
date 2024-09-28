import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {

	static BufferedReader br;
	static StringTokenizer st;

	static int n, k;
	static int[] durabilities;
	static int[] person;
	static int durabilityZeroCount;
	static int testCount;

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		st = new StringTokenizer(br.readLine());
		n = Integer.parseInt(st.nextToken());
		k = Integer.parseInt(st.nextToken());
		durabilities = new int[2 * n];
		st = new StringTokenizer(br.readLine());
		for (int i = 0; i < 2 * n; i++) {
			durabilities[i] = Integer.parseInt(st.nextToken());
		}
		person = new int[2 * n];
		durabilityZeroCount = 0;
		testCount = 0;
		while (true) {
			durabilityTest();
			testCount++;
			if (durabilityZeroCount >= k) {
				break;
			}
		}
		System.out.println(testCount);
	}

	private static void durabilityTest() {
		// 무빙워크가 한 칸 회전한
		final int d = durabilities[2 * n - 1];
		final int p = person[2 * n - 1];
		System.arraycopy(durabilities, 0, durabilities, 1, 2 * n - 1);
		System.arraycopy(person, 0, person, 1, 2 * n - 1);
		durabilities[0] = d;
		person[0] = p;
		// n번 칸에 사람이 있으면 내린다
		if (person[n - 1] == 1) {
			person[n - 1] = 0;
		}
		// 무빙워크가 회전하는 방향으로 한 칸 이동할 수 있으면 이동한다
		for (int i = n - 1; i > 0; i--) {
			if (person[i - 1] == 1 && person[i] == 0 && durabilities[i] > 0) {
				person[i - 1] = 0;
				person[i] = 1;
				durabilities[i]--;
				if (durabilities[i] == 0) {
					durabilityZeroCount++;
				}
			}
		}
		// n번 칸에 사람이 있으면 내린다
		if (person[n - 1] == 1) {
			person[n - 1] = 0;
		}
		// 1번 칸에 사람이 없고 안정성이 0이 아니라면 사람을 한 명 더 올린다
		if (person[0] == 0 && durabilities[0] > 0) {
			person[0] = 1;
			durabilities[0]--;
			if (durabilities[0] == 0) {
				durabilityZeroCount++;
			}
		}
	}
}