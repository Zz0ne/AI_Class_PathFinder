#ifndef NODE_H
#define NODE_H

template <typename T> class Node {
public:
  Node *parent;
  T state;
  int cost;

  Node(Node &parent);
  ~Node();
};

#endif // NODE_H
