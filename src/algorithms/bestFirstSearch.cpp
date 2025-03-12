#include "bestFirstSearch.h"

#include <queue>
#include <unordered_set>

template <typename T> bool bfs::search(Problem<T> &problem)
{
    Node<T> *initialNode = problem.getInitial();

    std::priority_queue<Node<T> *> frontier;

    std::unordered_set<Node<T> *> reached;
    reached.insert(initialNode);

    while (!frontier.empty())
    {
        auto node = frontier.pop();

        if (problem.isGoal(node))
        {
            return true;
        }

        auto nextNodes = problem.expand();
        for (auto currNode : nextNodes)
        {
            auto reachedNode = reached.find(currNode);
            if (reachedNode == reached.end() || currNode.cost < reachedNode.cost)
            {
                reached.insert(currNode);
                frontier.push(currNode);
            }
        }
    }
    return false;
}
