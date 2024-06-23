class LinkedList {
    static class Node {
        int data;
        Node next;

        Node(int data) {
            this.data = data;
            next = null;
        }
    }

    static Node head;

    public static int countNodes(Node head) {
        // Assuming that head != null
        int count = 1;
        Node current = head;
        while (current.next != null) {
            current = current.next;
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // Create the linked list
        head = new Node(7);
        Node nodeA = new Node(6);
        Node nodeB = new Node(3);
        Node nodeC = new Node(3);

        // Link the nodes
        head.next = nodeA;
        nodeA.next = nodeB;
        nodeB.next = nodeC;

        // Count the number of nodes
        int numNodes = countNodes(head);
        System.out.println("Number of nodes in the linked list: " + numNodes);
    }
}
