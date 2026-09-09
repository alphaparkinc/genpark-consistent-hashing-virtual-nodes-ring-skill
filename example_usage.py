"""Example usage for Consistent Hashing Ring Skill."""
from client import ConsistentHashRing

def main():
    print("Executing Consistent Hashing Ring...")
    ring = ConsistentHashRing(replicas=50)
    ring.add_node("AgentCluster_Node_1")
    ring.add_node("AgentCluster_Node_2")
    ring.add_node("AgentCluster_Node_3")

    targets = [f"task_payload_{i}" for i in range(10)]
    assignments = {t: ring.get_node(t) for t in targets}
    print("Assignments:", assignments)
    assert len(set(assignments.values())) > 1, "Failed to distribute keys"
    print("Consistent Hashing Ring verified successfully!")

if __name__ == "__main__":
    main()
