#include "puzzle8.h"

#include <algorithm>
#include <iostream>

std::shared_ptr<Node<BoardState> > Puzzle8::_moveUp(std::shared_ptr<Node<BoardState> > node)
{
    auto emptyTile = std::find(node->state.begin(), node->state.end(), 0);

    int emptyIndex = std::distance(node->state.begin(), emptyTile);
    int row        = emptyIndex / ROW_SIZE;

    // if the tile is in the first row
    if (row == 0) return nullptr;

    std::shared_ptr<Node<BoardState> > newNode = std::make_shared<Node<BoardState> >(*node);
    newNode->parent                            = node;
    newNode->cost++;

    std::swap(newNode->state[emptyIndex], newNode->state[emptyIndex - ROW_SIZE]);

    return newNode;
}

std::shared_ptr<Node<BoardState> > Puzzle8::_moveDown(std::shared_ptr<Node<BoardState> > node)
{
    auto emptyTile = std::find(node->state.begin(), node->state.end(), 0);

    int emptyIndex = std::distance(node->state.begin(), emptyTile);
    int row        = emptyIndex / ROW_SIZE;

    // if the tile is in the last row
    if (row == ROW_SIZE - 1) return nullptr;

    std::shared_ptr<Node<BoardState> > newNode = std::make_shared<Node<BoardState> >(*node);
    newNode->parent                            = node;
    newNode->cost++;

    std::swap(newNode->state[emptyIndex], newNode->state[emptyIndex + ROW_SIZE]);

    return newNode;
}

std::shared_ptr<Node<BoardState> > Puzzle8::_moveLeft(std::shared_ptr<Node<BoardState> > node)
{
    auto emptyTile = std::find(node->state.begin(), node->state.end(), 0);

    int emptyIndex = std::distance(node->state.begin(), emptyTile);
    int col        = emptyIndex % COL_SIZE;

    // if the tile is in the first col
    if (col == 0) return nullptr;

    std::shared_ptr<Node<BoardState> > newNode = std::make_shared<Node<BoardState> >(*node);
    newNode->parent                            = node;
    newNode->cost++;

    std::swap(newNode->state[emptyIndex], newNode->state[emptyIndex - 1]);

    return newNode;
}

std::shared_ptr<Node<BoardState> > Puzzle8::_moveRight(std::shared_ptr<Node<BoardState> > node)
{
    auto emptyTile = std::find(node->state.begin(), node->state.end(), 0);

    int emptyIndex = std::distance(node->state.begin(), emptyTile);
    int col        = emptyIndex % COL_SIZE;

    // if the tile is in the last col
    if (col == COL_SIZE - 1) return nullptr;

    std::shared_ptr<Node<BoardState> > newNode = std::make_shared<Node<BoardState> >(*node);
    newNode->parent                            = node;
    newNode->cost++;

    std::swap(newNode->state[emptyIndex], newNode->state[emptyIndex + 1]);

    return newNode;
}

void Puzzle8::_printBoard(BoardState &board)
{
    for (int i = 0; i < COL_SIZE; ++i) {
        for (int j = 0; j < ROW_SIZE; ++j) {
            std::cout << board[i * ROW_SIZE + j] << " ";
        }
        std::cout << "\n";
    }
}

Puzzle8::Puzzle8(BoardState initialState, BoardState goalState)
    : Problem<BoardState>(initialState, goalState)
{
}

bool Puzzle8::isGoal(std::shared_ptr<Node<BoardState> > node)
{
    if (node->state == _goalState) {
        _goalNode = std::make_shared<Node<BoardState> >(node);
        return true;
    }
    return false;
}

std::vector<std::shared_ptr<Node<BoardState> > > Puzzle8::expand(
    std::shared_ptr<Node<BoardState> > node)
{
    std::vector<std::shared_ptr<Node<BoardState> > > expandedNodes;

    if (auto upNode = _moveUp(node)) {
        expandedNodes.push_back(upNode);
    }

    if (auto downNode = _moveDown(node)) {
        expandedNodes.push_back(downNode);
    }

    if (auto leftNode = _moveLeft(node)) {
        expandedNodes.push_back(leftNode);
    }

    if (auto rightNode = _moveRight(node)) {
        expandedNodes.push_back(rightNode);
    }

    return expandedNodes;
}

void Puzzle8::printSolution()
{
    auto node = _goalNode;

    if (!node) {
        std::cout << "No solution found.\n";
        return;
    }

    std::vector<std::shared_ptr<Node<BoardState> > > path;

    while (node) {
        path.push_back(node);
        node = node->parent;
    }

    std::reverse(path.begin(), path.end());

    for (const auto &step : path) {
        _printBoard(step->state);
        std::cout << "-----\n";
    }
}
