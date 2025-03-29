#pragma once
#include <array>
#include <memory>

#include "../algorithms/helpers/Problem.h"

#define ROW_SIZE 3
#define COL_SIZE 3

using BoardState = std::array<int, ROW_SIZE * COL_SIZE>;

class Puzzle8 : public Problem<BoardState>
{
   private:
    std::shared_ptr<Node<BoardState> > _moveUp(std::shared_ptr<Node<BoardState> > node);

    std::shared_ptr<Node<BoardState> > _moveDown(std::shared_ptr<Node<BoardState> > node);

    std::shared_ptr<Node<BoardState> > _moveLeft(std::shared_ptr<Node<BoardState> > node);

    std::shared_ptr<Node<BoardState> > _moveRight(std::shared_ptr<Node<BoardState> > node);

    static void _printBoard(BoardState &board);

   public:
    Puzzle8(BoardState initialState, BoardState goalState);

    bool isGoal(std::shared_ptr<Node<BoardState> > node) override;

    std::vector<std::shared_ptr<Node<BoardState> > > expand(
        std::shared_ptr<Node<BoardState> > node) override;

    void printSolution() override;
};
