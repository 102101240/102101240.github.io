package com.example.sudu1;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

public class SudokuSolver {
    private int[][] board;
    private int SIZE=9;
    public SudokuSolver(int[][] board) {
        this.board = board;
    }

    public void solve() {
        solveRecursive(board);
    }

    private boolean solveRecursive(int[][] board) {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (board[row][col] == 0) {
                    for (int num = 1; num <= SIZE; num++) {
                        if (isValidPlacement(board, row, col, num)) {
                            board[row][col] = num;
                            if (solveRecursive(board)) {
                                return true;
                            }
                            board[row][col] = 0;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    private boolean isValidPlacement(int[][] board, int row, int col, int num) {
        // 检查行是否合法
        for (int i = 0; i < SIZE; i++) {
            if (board[row][i] == num) {
                return false;
            }
        }

        // 检查列是否合法
        for (int i = 0; i < SIZE; i++) {
            if (board[i][col] == num) {
                return false;
            }
        }

        // 检查3x3方格是否合法
        int startRow = row - (row % 3);
        int startCol = col - (col % 3);
        for (int i = startRow; i < startRow + 3; i++) {
            for (int j = startCol; j < startCol + 3; j++) {
                if (board[i][j] == num) {
                    return false;
                }
            }
        }

        return true;
    }

    public int[][] getBoard() {
        return board;
    }
}