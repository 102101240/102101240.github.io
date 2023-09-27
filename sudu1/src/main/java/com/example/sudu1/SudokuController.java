package com.example.sudu1;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.concurrent.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Controller
public class SudokuController {

    @GetMapping("/")
    public String getSudoku(Model model) {
        List<int[][]> sudokuList = generateSudoku();
        model.addAttribute("sudokuList", sudokuList);
        return "sudoku";
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
