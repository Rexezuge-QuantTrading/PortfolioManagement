import express from 'express';
import { container } from '../container/container';
import { UserController } from '../controllers/UserController';

const router = express.Router();

const controller = container.resolve(UserController);

router.get('/:id', controller.getUser);

export default router;
