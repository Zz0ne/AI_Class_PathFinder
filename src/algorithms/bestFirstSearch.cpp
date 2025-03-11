#include "bestFirstSearch.h"

#include "bestFirstSearch.h"

#include <queue>
#include <unordered_set>

template <typename T> Node<T> bfs::search(Problem<T> problem)
{
    Node<T> initialNode = problem.getInitial();

    std::priority_queue<Node<T>> frontier;

    std::unordered_set<Node<T>> reached;
    reached.insert(initialNode);

    while (!frontier.empty())
    {
        auto node = frontier.pop();

        if (problem.isGoal(node))
            return node;

        auto nextNodes = problem.expand();
        for (auto nextNode : nextNodes)
        {
            if (reached.find(nextNode) == reached.end())
            {
            }
        }
    }
}
