import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {

	private static final int MAX_ID = 100_005;
	private static final int ADD_NODE = 100;
	private static final int CHANGE_COLOR = 200;
	private static final int CHECK_COLOR = 300;
	private static final int CHECK_POINT = 400;

	private static final Node[] nodes = new Node[MAX_ID];
	private static final boolean[] isRoot = new boolean[MAX_ID];

	static {
		for (int i = 0; i < MAX_ID; i++) {
			nodes[i] = new Node();
		}
	}

	public static void main(String[] args) throws Exception {
		// System.setIn(Files.newInputStream(Paths.get("input.txt")));
		final BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		final int Q = Integer.parseInt(br.readLine());
		StringTokenizer st;
		int command, mid, pid, color, maxDepth;
		for (int q = 0; q < Q; q++) {
			st = new StringTokenizer(br.readLine());
			command = Integer.parseInt(st.nextToken());
			switch (command) {
				case ADD_NODE:
					mid = Integer.parseInt(st.nextToken());
					pid = Integer.parseInt(st.nextToken());
					color = Integer.parseInt(st.nextToken());
					maxDepth = Integer.parseInt(st.nextToken());
					if (pid == -1) {
						isRoot[mid] = true;
					}
					if (isRoot[mid] || checkMaxDepth(nodes[pid], 1)) {
						nodes[mid].mid = mid;
						nodes[mid].pid = isRoot[mid] ? 0 : pid;
						nodes[mid].color = color;
						nodes[mid].lastUpdate = q;
						nodes[mid].maxDepth = maxDepth;
						if (!isRoot[mid]) {
							nodes[pid].childIds.add(mid);
						}
					}
					break;
				case CHANGE_COLOR:
					mid = Integer.parseInt(st.nextToken());
					color = Integer.parseInt(st.nextToken());
					nodes[mid].color = color;
					nodes[mid].lastUpdate = q;
					break;
				case CHECK_COLOR:
					mid = Integer.parseInt(st.nextToken());
					System.out.println(getColor(nodes[mid])[0]);
					break;
				case CHECK_POINT:
					int result = 0;
					for (int i = 1; i < MAX_ID; i++) {
						if (isRoot[i]) {
							final ColorCountDto colorCountDto = update(nodes[i], nodes[i].color, nodes[i].lastUpdate);
							result += colorCountDto.result;
						}
					}
					System.out.println(result);
					break;
			}
		}
	}

	private static boolean checkMaxDepth(final Node node, final int needDepth) {
		if (node.mid == 0) {
			return true;
		}
		if (node.maxDepth <= needDepth) {
			return false;
		}
		return checkMaxDepth(nodes[node.pid], needDepth + 1);
	}

	private static int[] getColor(final Node node) {
		if (node.mid == 0) {
			return new int[] { 0, 0 };
		}
		int[] parentColorInfo = getColor(nodes[node.pid]);
		if (parentColorInfo[1] > node.lastUpdate) {
			return parentColorInfo;
		}
		return new int[] { node.color, node.lastUpdate };
	}

	private static ColorCountDto update(final Node node, int color, int lastUpdate) {
		if (lastUpdate < node.lastUpdate) {
			lastUpdate = node.lastUpdate;
			color = node.color;
		}
		int result = 0;
		ColorCount colorCount = new ColorCount();
		colorCount.count[color]++;
		for (final int childId : node.childIds) {
			final Node child = nodes[childId];
			final ColorCountDto childColorCountDto = update(child, color, lastUpdate);
			colorCount = colorCount.merge(childColorCountDto.colorCount);
			result += childColorCountDto.result;
		}
		result += colorCount.point();
		return new ColorCountDto(result, colorCount);
	}
}

class Node {

	int mid;
	int pid;
	int color;
	int lastUpdate;
	int maxDepth;
	List<Integer> childIds = new ArrayList<>();
}

class ColorCount {

	final int[] count = new int[6];

	ColorCount merge(final ColorCount other) {
		final ColorCount result = new ColorCount();
		for (int i = 1; i <= 5; i++) {
			result.count[i] = this.count[i] + other.count[i];
		}
		return result;
	}

	int point() {
		int value = 0;
		for (int i = 1; i <= 5; i++) {
			if (count[i] > 0) {
				value++;
			}
		}
		return value * value;
	}
}

class ColorCountDto {

	int result;
	ColorCount colorCount;

	public ColorCountDto(final int result, final ColorCount colorCount) {
		this.result = result;
		this.colorCount = colorCount;
	}
}