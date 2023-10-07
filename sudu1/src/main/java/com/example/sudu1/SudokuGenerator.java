package com.example.sudu1;

import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;



import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;

public class SudokuGenerator {
    private static final int SIZE = 9;
    private static final int EMPTY_CELL = 0;
    private static final int MINIMUM_GIVENS = 17; // 最少的已知数字数量

    public int[][] generate() {
        int[][] board = new int[SIZE][SIZE];
        fillDiagonalRegions(board); // 填充对角区域
        solve(board); // 解数独
        removeCells(board); // 移除格子
        return board;
    }
    public int[][] solve1(int[][] board){
        solve(board); // 解数独

        return board;
    }
    private void fillDiagonalRegions(int[][] board) {
        int[] values = IntStream.rangeClosed(1, SIZE).toArray();
        shuffleArray(values); // 随机打乱数字顺序

        for (int i = 0; i < SIZE; i += 3) {
            fillBox(board, i, i, values);
        }
    }

    private void fillBox(int[][] board, int startRow, int startCol, int[] values) {
        int index = 0;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[startRow + i][startCol + j] = values[index];
                index++;
            }
        }
    }

    private void solve(int[][] board) {
        solveRecursive(board);
    }

    private boolean solveRecursive(int[][] board) {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (board[row][col] == EMPTY_CELL) {
                    for (int num = 1; num <= SIZE; num++) {
                        if (isValidPlacement(board, row, col, num)) {
                            board[row][col] = num;
                            if (solveRecursive(board)) {
                                return true;
                            }
                            board[row][col] = EMPTY_CELL;
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

    private void removeCells(int[][] board) {
        ThreadLocalRandom random = ThreadLocalRandom.current();

        int givens = SIZE * SIZE;
        while (givens > MINIMUM_GIVENS) {
            int row = random.nextInt(SIZE);
            int col = random.nextInt(SIZE);

            if (board[row][col] != EMPTY_CELL) {
                int temp = board[row][col];
                board[row][col] = EMPTY_CELL;

                int[][] copy = new int[SIZE][SIZE];
                for (int i = 0; i < SIZE; i++) {
                    System.arraycopy(board[i], 0, copy[i], 0, SIZE);
                }

                if (hasUniqueSolution(copy)) {
                    givens--;
                } else {
                    board[row][col] = temp;
                }
            }
        }
    }

    private boolean hasUniqueSolution(int[][] board) {
        int[][] copy = new int[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            System.arraycopy(board[i], 0, copy[i], 0, SIZE);
        }
        return solveRecursive(copy);
    }

    private void shuffleArray(int[] array) {
        ThreadLocalRandom random = ThreadLocalRandom.current();
        for (int i = array.length - 1; i > 0; i--) {
            int index = random.nextInt(i + 1);
            int temp = array[index];
            array[index] = array[i];
            array[i] = temp;
        }
    }
}