-- AlterTable
ALTER TABLE "Catalog" ADD COLUMN "link" TEXT;

-- CreateTable
CREATE TABLE "Mode" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "idUser" TEXT NOT NULL,
    "state" TEXT NOT NULL DEFAULT 'standart'
);
