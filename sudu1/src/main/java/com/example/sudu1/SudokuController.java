package com.example.sudu1;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.concurrent.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Controller
public class SudokuController {

    private List<int[][]> sudokuList;

    @GetMapping("/")
    public String getSudoku(Model model) {
        sudokuList = generateSudoku();
        model.addAttribute("sudokuList", sudokuList);
        return "sudoku";
    }

    @PostMapping("/solve")
    public String solveSudoku(Model model) {
        System.out.println("Start solving Sudoku");

        List<int[][]> solvedSudokus = solveSudokuConcurrently();

        System.out.println("Sudoku solving completed");

        model.addAttribute("solvedSudokus", solvedSudokus);
        return "solvedSudoku";
    }

    private List<int[][]> solveSudokuConcurrently() {
        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        CompletionService<int[][]> completionService = new ExecutorCompletionService<>(executor);

        int numSudokus = 9;
        List<Callable<int[][]>> sudokuSolverTasks = new ArrayList<>();
        if (sudokuList == null || sudokuList.isEmpty()) {
            System.out.println("sudokuList is empty");
            // 可以尝试生成数独列表或从其他地方获取数独列表
        }
        if (sudokuList != null || !sudokuList.isEmpty()) {
            System.out.println("sudokuList is unempty");
            // 可以尝试生成数独列表或从其他地方获取数独列表
        }
        for (int[][] sudoku : sudokuList) {
            sudokuSolverTasks.add(() -> {
                SudokuSolver solver = new SudokuSolver(sudoku);
                solver.solve();
                return solver.getBoard();
            });
        }

        List<int[][]> solvedSudoku = new ArrayList<>();
        boolean interrupted = false; // 标志变量，指示解决过程是否被中断

        List<Future<int[][]>> results = new ArrayList<>();

        for (Callable<int[][]> task : sudokuSolverTasks) {
            completionService.submit(task);
            System.out.println("Sudoku solve task submitted");
        }

        for (int i = 0; i < numSudokus; i++) {
            System.out.println("Trying to take completedTask");
            System.out.println("Number of submitted tasks: " + results.size());
            try {
                Future<int[][]> completedTask = completionService.take();
                System.out.println("Waiting for completedTask");
                int[][] solvedBoard = completedTask.get();
                solvedSudoku.add(solvedBoard);
            } catch (InterruptedException e) {
                System.out.println("Trying to take completedTask");
                Thread.currentThread().interrupt();
                interrupted = true; // 设置中断标志为true
                e.printStackTrace();
                break; // 中断发生，退出循环
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }

        executor.shutdown();

        if (interrupted) {
            // 返回部分解决的数独列表和中断标志
            return solvedSudoku;
        } else {
            // 返回完整的解决数独列表
            return solvedSudoku;
        }
    }

    private static List<int[][]> generateSudoku() {
        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        List<Callable<int[][]>> sudokuTasks = new ArrayList<>();

        int numSudokus = 9; // 生成数独的数量

        for (int i = 0; i < numSudokus; i++) {
            final int index = i;
            sudokuTasks.add(() -> {
                SudokuGenerator generator = new SudokuGenerator();
                return generator.generate();
            });
        }

        try {
            List<Future<int[][]>> results = executor.invokeAll(sudokuTasks);
            executor.shutdown();

            List<int[][]> sudokuList = new ArrayList<>();
            for (Future<int[][]> future : results) {
                int[][] board = future.get();
                sudokuList.add(board);
            }

            return sudokuList;
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
            return new ArrayList<>(); // 返回一个空的数独列表
        }
    }
}