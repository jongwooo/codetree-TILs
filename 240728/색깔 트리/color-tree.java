import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {

	private static final int ADD_NODE = 100;
	private static final int CHANGE_COLOR = 200;
	private static final int CHECK_COLOR = 300;
	private static final int CHECK_POINT = 400;

	private static Map<Integer, ColorNode> colorNodeMap;
	private static List<ColorNode> top;

	public static void main(String[] args) throws Exception {
//		System.setIn(new FileInputStream("input.txt"));
		final BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		final int Q = Integer.parseInt(br.readLine());
		colorNodeMap = new HashMap<>();
		top = new LinkedList<>();
		StringTokenizer st;
		int mid, pid, color, depth;
		for (int q = 0; q < Q; q++) {
			st = new StringTokenizer(br.readLine());
			int command = Integer.parseInt(st.nextToken());
			switch (command) {
			case ADD_NODE:
				mid = Integer.parseInt(st.nextToken());
				pid = Integer.parseInt(st.nextToken());
				color = Integer.parseInt(st.nextToken());
				depth = Integer.parseInt(st.nextToken());
				addNode(mid, pid, color, depth);
				break;
			case CHANGE_COLOR:
				mid = Integer.parseInt(st.nextToken());
				color = Integer.parseInt(st.nextToken());
				changeColor(mid, color);
				break;
			case CHECK_COLOR:
				mid = Integer.parseInt(st.nextToken());
				checkColor(mid);
				break;
			case CHECK_POINT:
				checkPoint();
				break;
			}
		}
	}

	private static void addNode(final int mid, final int pid, final int color, final int depth) {
		if (pid == -1) {
			final ColorNode node = new ColorNode(mid, color, depth);
			colorNodeMap.put(mid, node);
			top.add(node);
			return;
		}
		final ColorNode parent = colorNodeMap.get(pid);
		if (parent == null) {
			return;
		}
		if (checkMaxDepth(parent)) {
			final ColorNode now = new ColorNode(mid, parent, color, depth);
			colorNodeMap.put(mid, now);
			parent.child.add(now);
		}
	}

	private static boolean checkMaxDepth(final ColorNode node) {
		ColorNode cur = node;
		int depth = 1;
		while (cur.parent != null) {
			if (cur.depth <= depth) {
				return false;
			}
			cur = cur.parent;
			depth++;
		}
		return true;
	}

	private static void changeColor(final int mid, final int color) {
		final ColorNode now = colorNodeMap.get(mid);
		now.color = color;
		for (final ColorNode node : now.child) {
			changeColor(node.mid, color);
		}
	}

	private static void checkColor(final int mid) {
		final ColorNode node = colorNodeMap.get(mid);
		System.out.println(node.color);
	}

	private static void checkPoint() {
		int result = 0;
		boolean[] colors;
		for (final ColorNode node : top) {
			colors = new boolean[6];
			result += dfs(node, colors);
		}
		System.out.println(result);
	}

	private static int dfs(final ColorNode node, final boolean[] colors) {
		if (node.child.size() == 0) {
			colors[node.color] = true;
			return 1; // 해당 노드를 루트로 하는 서브트리가 없기 때문에 가치는 1이다.
		}
		int result = 0;
		final boolean[] newColors = new boolean[6];
		for (final ColorNode now : node.child) {
			result += dfs(now, newColors);
		}
		newColors[node.color] = true;
		int value = 0;
		for (int c = 1; c <= 5; c++) {
			if (newColors[c]) {
				colors[c] = true;
				value++;
			}
		}
		result += value * value;
		return result;
	}
}

class ColorNode {

	final int mid;
	ColorNode parent = null;
	final List<ColorNode> child = new LinkedList<>();
	int color;
	final int depth;

	public ColorNode(final int mid, final int color, final int depth) {
		this.mid = mid;
		this.color = color;
		this.depth = depth;
	}

	public ColorNode(final int mid, final ColorNode parent, final int color, final int depth) {
		this.mid = mid;
		this.parent = parent;
		this.color = color;
		this.depth = depth;
	}
}