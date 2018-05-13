package com.theaigames.engine.io;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class HumanPlayer implements Bot {

    private boolean LOG_MOVES;
    private String idString;

    public HumanPlayer (String idString, boolean LOG_MOVES) {
        this.LOG_MOVES = LOG_MOVES;
        this.idString = idString;
        System.out.println("Playing as player "+ (idString.equals("1") ? "X" : "O") + ".");
    }

    public void writeToBot(String line) throws IOException {
        String[] splitLine = line.split(" ");
        if (splitLine.length == 4
                && splitLine[0].equals("update")
                && splitLine[1].equals("game")) {
            if (splitLine[2].equals("field")) {
                String[] marks = splitLine[3].split(",");
                int index = 0;
                StringBuilder sb = new StringBuilder(1600);
                String s1 = "\u2520\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2542\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2542\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2528\n";
                String s2 = "\u2523\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u254b\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u254b\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u253f\u2501\u2501\u2501\u252b\n";

                sb.append("    0   1   2   3   4   5   6   7   8\n  ");
                sb.append("\u250f\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u2533\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u2533\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u252f\u2501\u2501\u2501\u2513\n0 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "1 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "2 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s2 + "3 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "4 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "5 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s2 + "6 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "7 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append(s1 + "8 ");
                index = boardMakerHelper(sb, marks, index);
                sb.append("\u2517\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u253b\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u253b\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u2537\u2501\u2501\u2501\u251b\n");

                System.out.println(sb.toString());
            } else if (splitLine[2].equals("macroboard")) {
                ArrayList<Integer> botWon = new ArrayList<Integer>();
                ArrayList<Integer> humanWon = new ArrayList<Integer>();
                ArrayList<Integer> available = new ArrayList<Integer>();
                ArrayList<Integer> draws = new ArrayList<Integer>();

                String[] board = splitLine[3].split(",");
                for (int i = 0; i < board.length; i++) {
                    if (board[i].equals("0")) {
                        draws.add(i);
                    } else if (board[i].equals(idString)) {
                        humanWon.add(i);
                    } else if (board[i].equals("-1")) {
                        available.add(i);
                    } else {
                        botWon.add(i);
                    }
                }

                Object[] bWon = botWon.stream().map(i -> getBoardName(i)).toArray();
                Object[] hWon = humanWon.stream().map(i -> getBoardName(i)).toArray();
                Object[] d = draws.stream().map(i -> getBoardName(i)).toArray();
                Object[] av = available.stream().map(i -> getBoardName(i)).toArray();

                if (bWon.length == 0) {
                    System.out.println("The bot has won no microboards.");
                } else if (bWon.length == 1) {
                    System.out.println("The bot has won the " + bWon[0] + " microboard.");
                } else if (bWon.length == 2) {
                    System.out.println("The bot has won the " + bWon[0] + " and " + bWon[1] + " microboards.");
                } else {
                    StringBuilder bsb = new StringBuilder(50);
                    bsb.append("The bot has won the ");

                    for (int i = 0; i < bWon.length; i++) {
                        bsb.append((String) bWon[i]);
                        if (i == bWon.length - 2) {
                            bsb.append(", and ");
                        } else if (i != bWon.length - 1) {
                            bsb.append(", ");
                        }
                    }

                    bsb.append(" microboards.");
                    System.out.println(bsb.toString());
                }

                if (hWon.length == 0) {
                    System.out.println("You have won no microboards.");
                } else if (hWon.length == 1) {
                    System.out.println("You have won the " + hWon[0] + " microboard.");
                } else if (hWon.length == 2) {
                    System.out.println("You have won the " + hWon[0] + " and " + hWon[1] + " microboards.");
                } else {
                    StringBuilder hsb = new StringBuilder(50);
                    hsb.append("You have won the ");

                    for (int i = 0; i < hWon.length; i++) {
                        hsb.append((String) hWon[i]);
                        if (i == hWon.length - 2) {
                            hsb.append(", and ");
                        } else if (i != hWon.length - 1) {
                            hsb.append(", ");
                        }
                    }

                    hsb.append(" microboards.");
                    System.out.println(hsb.toString());
                }

                if (d.length == 0) {
                    System.out.println("No microboards are draws.");
                } else if (d.length == 1) {
                    System.out.println("The " + d[0] + " microboard is a draw.");
                } else if (d.length == 2) {
                    System.out.println("The " + d[0] + " and " + d[1] + " microboards are draws.");
                } else {
                    StringBuilder dsb = new StringBuilder(50);
                    dsb.append("The ");

                    for (int i = 0; i < d.length; i++) {
                        dsb.append((String) d[i]);
                        if (i == d.length - 2) {
                            dsb.append(", and ");
                        } else if (i != d.length - 1) {
                            dsb.append(", ");
                        }
                    }

                    dsb.append(" microboards are draws.");
                    System.out.println(dsb.toString());
                }

                if (av.length == 0) {
                    System.out.println("You may not play in any boards.");
                } else if (av.length == 1) {
                    System.out.println("You must play in the " + av[0] + " microboard.");
                } else if (av.length == 2) {
                    System.out.println("You must play in the " + av[0] + " or " + av[1] + " microboard.");
                } else {
                    StringBuilder asb = new StringBuilder(50);
                    asb.append("You must play in the ");

                    for (int i = 0; i < av.length; i++) {
                        asb.append((String) av[i]);
                        if (i == av.length - 2) {
                            asb.append(", or ");
                        } else if (i != av.length - 1) {
                            asb.append(", ");
                        }
                    }

                    asb.append(" microboard.");
                    System.out.println(asb.toString());
                }
            }
        }
    }

    private int boardMakerHelper(StringBuilder sb, String[] marks, int index) {
        for (int i = 0; i < 9; i++) {
            if (i % 3 == 0) {
                sb.append("\u2503");
            } else {
                sb.append("\u2502");
            }
            sb.append(" "+(marks[index].equals("1") ? "X" : (marks[index].equals("2") ? "O" : " "))+" ");
            index++;
        }
        sb.append("\u2503\n  ");
        return index;
    }

    private String getBoardName(int i) {
        switch(i) {
            case 0:
                return "top left";
            case 1:
                return "top middle";
            case 2:
                return "top right";
            case 3:
                return "middle left";
            case 4:
                return "middle";
            case 5:
                return "middle right";
            case 6:
                return "bottom left";
            case 7:
                return "bottom middle";
            case 8:
                return "bottom right";
        }
        return "";
    }

    public String getResponse(long timeOut) {
        System.out.println("Make a move (syntax: [column] [row]):");
        Scanner s = new Scanner(System.in);
        return "place_move " + s.nextLine();
    }

    public void outputEngineWarning(String warning) {
        System.out.println("Warning: "+warning);
    }
}
