//
// Created by nunorl on 3/10/25.
//

#ifndef PROBLEM_H
#define PROBLEM_H

#include <vector>

#include "Node.h"

template <typename T> class Problem
{
  private:
    T _initialState;
    T _goalState;

  public:
    Problem(T initialState, T goalState);

    Node<T> *getInitial();
    Node<T> *getResult();

    virtual bool isGoal(Node<T> &node);
    virtual std::vector<Node<T> *> expand(Node<T> &node);
};

#endif // PROBLEM_H
